from dataclasses import dataclass

@dataclass
class AtlasConfig:
    # API Keys
    openai_api_key: str
    broker: str  # e.g., "alpaca" or "zerodha"
    broker_api_key: str  # REPLACE WITH ACTUAL BROKER API KEY
    broker_api_secret: str  # REPLACE WITH ACTUAL BROKER API SECRET
    database_api_key: str  # REPLACE WITH ACTUAL DATABASE API KEY (if applicable)
    database_url: str  # REPLACE WITH ACTUAL DATABASE URL (if applicable)

    # Google Sheets
    gsheet_creds_file: str  # Path to the Google Sheets credentials file (e.g., "credentials.json") - REPLACE WITH ACTUAL CREDENTIALS
    gsheet_doc_name: str

    # Risk Parameters
    max_risk_per_trade: float  # e.g., 0.02 (2%)
    min_reward_ratio: float  # e.g., 3.0 (3:1 RR)
    max_positions: int  # max concurrent open trades

    # Market/Trading Settings
    base_currency: str  # "USD" or "INR"
    paper_trading: bool  # True for paper trading mode
    market: str  # "US" or "IN"
    trading_hours: tuple  # (start_hour, end_hour) as per market timezone

# Example instantiation
config = AtlasConfig(
    openai_api_key="sk-***",
    broker="alpaca",
    broker_api_key="AK***", broker_api_secret="SK***",
    gsheet_creds_file="credentials.json",
    gsheet_doc_name="Atlas Trade Log",
    max_risk_per_trade=0.02, min_reward_ratio=3.0,
    max_positions=5,
    base_currency="USD", paper_trading=True,
    market="US", trading_hours=(9.5, 16)  # 9:30-16:00 for NYSE
)