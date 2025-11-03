import openai
from time import sleep
from config import AtlasConfig
from agents.technical_analysis_agent import TechnicalAnalysisAgent
from agents.fundamental_analysis_agent import FundamentalAnalysisAgent
from agents.sentiment_analysis_agent import SentimentAnalysisAgent
from memory.vector_database import VectorDatabase
from memory.structured_database import StructuredDatabase
from memory.google_sheets_memory import GoogleSheetsMemory
from risk_agent import RiskAgent
from execution_agent import ExecutionAgent
from broker import AlpacaBroker  # Assuming Alpaca for now
from logger import SheetsLogger
import json

class Orchestrator:
    def __init__(self, config: AtlasConfig):
        self.config = config
        openai.api_key = config.openai_api_key

        # Initialize agents
        self.technical_agent = TechnicalAnalysisAgent()
        self.fundamental_agent = FundamentalAnalysisAgent()
        self.sentiment_agent = SentimentAnalysisAgent()

        # Initialize memory layers
        self.vector_db = VectorDatabase()
        self.structured_db = StructuredDatabase()
        self.sheets_memory = GoogleSheetsMemory()
        
        # Initialize other components
        self.risk = RiskAgent(config)
        self.executor = ExecutionAgent(config)
        self.broker = AlpacaBroker(config.broker_api_key, config.broker_api_secret, config.paper_trading)
        self.logger = SheetsLogger(config.gsheet_creds_file, config.gsheet_doc_name)

    def run(self):
        equity = 100000  # Example initial equity
        while True:
            # Fetch signals from agents
            signals = self.get_signals()
            for sig in signals:
                symbol, side, entry_price, stop_guess, target_guess, reason = sig

                # Retrieve context from memory for this symbol/sector (RAG)
                context = self.retrieve_context(symbol, reason)

                # Compose LLM prompt
                prompt = (f"Trade signal: {side} {symbol} at {entry_price}. "
                          f"Stop ~{stop_guess}, Target ~{target_guess}. Reason: {reason}.\n"
                          f"Context: {context}\n"
                          "Assess this trade and suggest position size, precise stop and target. Respond in JSON format.")
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": prompt}]
                    )
                except Exception as e:
                    # Fallback to local LLM or GPT-3 if GPT-4 fails
                    response = self.fallback_local_model(prompt)

                plan = self.parse_response(response)  # extract dict: {"symbol":..., "side":..., "stop":..., "target":..., "confidence":...}
                if not plan:
                    continue # Skip if LLM couldn't generate a plan

                # Risk check
                qty = self.risk.assess_trade(equity, symbol,
                                            side, entry_price, plan.get("stop"), plan.get("target"))
                if qty and qty > 0:
                    order_id = self.executor.place_order(symbol,
                                                        side, qty, order_type="MARKET",
                                                        stop_loss=plan.get("stop"), take_profit=plan.get("target"))
                    if order_id:
                        self.logger.log_trade(symbol, side, qty,
                                                entry_price,
                                                plan.get("stop"), plan.get("target"),
                                                plan.get("reason", "LLM trade"))

                        # Save rationale to memory
                        rationale = (f"{side} {symbol} at {entry_price}, SL={plan.get('stop')}, TP={plan.get('target')} -> {plan.get('reason')}")
                        self.vector_db.add_document(rationale)
                        self.structured_db.store({"symbol": symbol, "side": side, "entry_price": entry_price, "stop": plan.get("stop"), "target": plan.get("target"), "reason": plan.get("reason")})
                        self.sheets_memory.store_trade({"symbol": symbol, "side": side, "entry_price": entry_price, "stop": plan.get("stop"), "target": plan.get("target"), "reason": plan.get("reason")})
                        print(f"Trade executed successfully. Order ID: {order_id}")
                    else:
                        print("Order placement failed.")
                else:
                    print("Trade rejected by risk management.")

            sleep(1)  # wait or sync to next data update interval

    def get_signals(self):
        # In a real system, this would collect outputs from signal agents.
        # Here we just stub a list or pull from some signal queue.
        signals = []
        technical_signal = self.technical_agent.get_signal()
        if technical_signal:
            signals.append(technical_signal)

        fundamental_signal = self.fundamental_agent.get_signal()
        if fundamental_signal:
            signals.append(fundamental_signal)

        sentiment_signal = self.sentiment_agent.get_signal()
        if sentiment_signal:
            signals.append(sentiment_signal)
        return signals

    def retrieve_context(self, symbol, reason):
        # Implement RAG logic here
        query = f"{symbol} {reason} trade rationale"
        context = self.vector_db.search(query)
        return context

    def fallback_local_model(self, prompt):
        # Implement fallback to local LLM here
        return None

    def parse_response(self, response):
        # Implement parsing of LLM response here
        try:
            return json.loads(response["choices"][0]["message"]["content"])
        except (json.JSONDecodeError, KeyError, TypeError):
            print(f"Error parsing LLM response: {response}")
            return None