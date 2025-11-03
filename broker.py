from abc import ABC, abstractmethod

class BrokerBase(ABC):
    @abstractmethod
    def get_price(self, symbol):
        pass

    @abstractmethod
    def place_order(self, symbol, side, quantity, order_type, price=None,
                    stop_loss=None, take_profit=None):
        pass

# Alpaca implementation example
import requests
class AlpacaBroker(BrokerBase):
    def __init__(self, api_key, api_secret, paper=True):
        base_url = "https://paper-api.alpaca.markets" if paper else "https://api.alpaca.markets"
        self.base_url = base_url + "/v2"
        self.session = requests.Session()
        self.session.headers.update({
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": api_secret
        })

    def get_price(self, symbol):
        # call Alpaca’s market data API (v2) for last quote
        resp = requests.get(f"{self.base_url}/stocks/{symbol}/quotes/latest")
        data = resp.json()
        return data["quote"]["ap"]  # ask price as example

    def place_order(self, symbol, side, quantity, order_type="market",
                    price=None, stop_loss=None, take_profit=None):
        order = {
            "symbol": symbol,
            "qty": quantity,
            "side": side.lower(),  # "buy" or "sell"
            "type": order_type,  # "market" or "limit"
            "time_in_force": "day"
        }
        if order_type == "limit":
            order["limit_price"] = price

        # If stop-loss/take-profit provided, use bracket order
        if stop_loss or take_profit:
            order["order_class"] = "bracket"
            if take_profit:
                order["take_profit"] = {"limit_price": take_profit}
            if stop_loss:
                order["stop_loss"] = {"stop_price": stop_loss}

        resp = self.session.post(f"{self.base_url}/orders", json=order)
        if resp.status_code == 200:
            return resp.json().get("id")  # return order ID
        else:
            raise Exception(f"Order failed: {resp.text}")

# Zerodha implementation example (using hypothetical KiteConnect library)
class ZerodhaBroker(BrokerBase):
    def __init__(self, api_key, access_token):
        from kiteconnect import KiteConnect
        self.kite = KiteConnect(api_key=api_key)
        self.kite.set_access_token(access_token)

    def get_price(self, symbol):
        # symbol format might be different in Zerodha (exchange:token)
        quote = self.kite.quote(symbol)
        return quote[symbol]["last_price"]

    def place_order(self, symbol, side, quantity, order_type="MARKET",
                    price=None, stop_loss=None, take_profit=None):
        transaction_type = self.kite.TRANSACTION_TYPE_BUY if side.lower() == "buy" \
            else self.kite.TRANSACTION_TYPE_SELL
        order_params = {
            "tradingsymbol": symbol,
            "exchange": "NSE",
            "transaction_type": transaction_type,
            "quantity": quantity,
            "order_type": order_type,
            "product": "MIS",  # intraday product code
        }
        if order_type == "LIMIT":
            order_params["price"] = price

        # Zerodha doesn't support server-side bracket orders in 2025 for MIS; handle SL/TP manually
        order_id = self.kite.place_order(**order_params)

        # If stop_loss is set, immediately place a separate stop order (for MIS, use SL order)
        if stop_loss:
            sl_params = order_params.copy()
            sl_params.update({
                "order_type": "SL",
                "price": stop_loss, "trigger_price": stop_loss,
                "transaction_type": self.kite.TRANSACTION_TYPE_SELL if
                side.lower() == "buy" else self.kite.TRANSACTION_TYPE_BUY
            })
            self.kite.place_order(**sl_params)
        return order_id