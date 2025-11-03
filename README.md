# Atlas AI Trading System

## Description

The Atlas AI Trading System is an automated trading platform that leverages artificial intelligence to make informed trading decisions. It incorporates various agents, memory modules, and risk management strategies to optimize trading performance.

## Components

-   **Agents:**
    -   Fundamental Analysis Agent: Analyzes financial data and economic indicators.
    -   Technical Analysis Agent: Uses technical indicators and chart patterns to identify trading opportunities.
    -   Sentiment Analysis Agent: Gauges market sentiment from news and social media.
    -   Risk Agent: Manages risk exposure and ensures compliance with risk limits.
    -   Execution Agent: Executes trades based on signals from other agents.
    -   Allocation Agent: Determines the optimal allocation of capital across different assets.
    -   Self-Critique Agent: Evaluates the performance of the system and suggests improvements.
    -   RL Agent: Uses reinforcement learning to optimize trading strategies.
-   **Memory:**
    -   Vector Database: Stores and retrieves information using vector embeddings.
    -   Structured Database: Stores structured data, such as financial statements and trading history.
    -   Google Sheets Memory: Integrates with Google Sheets for data storage and retrieval.
-   **Other Modules:**
    -   Broker: Connects to a brokerage account for order execution.
    -   Monitoring: Tracks system performance and alerts for anomalies.
    -   News Filter: Filters relevant news articles.
    -   Backtesting: Simulates trading strategies on historical data.
    -   User Interface: Provides a user-friendly interface for monitoring and controlling the system.

## Setup Instructions

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Configure credentials:
    -   Create a `credentials.json` file in the project root directory.
    -   Add your API keys and account information to the file.  See `credentials.example.json` for the expected format.
3.  Run the system:
    ```bash
    python main.py
    ```# atlas-trading-system
