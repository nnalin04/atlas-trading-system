from config import AtlasConfig
from orchestrator import Orchestrator
from user_interface import UserInterface

if __name__ == "__main__":
    # Load configuration
    config = AtlasConfig(
        openai_api_key="sk-***",  # Replace with your OpenAI API key
        broker="alpaca",
        broker_api_key="AK***",  # Replace with your Alpaca API key
        broker_api_secret="SK***",  # Replace with your Alpaca API secret
        database_api_key="db-***",  # Replace with your Database API key
        database_url="https://***",  # Replace with your Database URL
        gsheet_creds_file="credentials.json",  # Replace with your Google Sheets credentials file
        gsheet_doc_name="Atlas Trade Log",
        max_risk_per_trade=0.02,
        min_reward_ratio=3.0,
        max_positions=5,
        base_currency="USD",
        paper_trading=True,
        market="US",
        trading_hours=(9.5, 16)  # 9:30-16:00 for NYSE
    )

    # Initialize components
    orchestrator = Orchestrator(config)
    user_interface = UserInterface()

    # Run the application
    while True:
        query = user_interface.get_user_query()
        if query.lower() == "exit":
            break
        # Process the query and display the response
        # In a real application, this would involve more complex logic
        response = f"Response to your query: {query}"
        user_interface.display_response(response)

    # Start the trading loop (in a separate thread or process)
    orchestrator.run()