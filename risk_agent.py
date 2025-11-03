from config import AtlasConfig

class RiskAgent:
    def __init__(self, config: AtlasConfig):
        self.max_risk = config.max_risk_per_trade  # e.g. 0.02 (2%)
        self.min_rr = config.min_reward_ratio  # e.g. 3.0 (3:1)

    def assess_trade(self, equity, symbol, side, entry_price, stop_price,
                    target_price):
        """Return adjusted quantity if trade is allowed, or 0 if rejected."""
        # Calculate risk per share/contract
        risk_per_unit = abs(entry_price - stop_price)
        if risk_per_unit <= 0:
            return 0  # invalid stop (e.g., stop not set below entry for long)

        # Position size for max risk
        max_loss_amount = equity * self.max_risk
        quantity = max_loss_amount // risk_per_unit  # integer division to get units
        if quantity <= 0:
            return 0  # equity too low for even 1 unit at this risk

        # Check risk-reward ratio
        if target_price and stop_price:
            expected_rr = abs(target_price - entry_price) / abs(entry_price -
                                                                stop_price)
            if expected_rr < self.min_rr:
                return 0  # reject trade, RR not favorable

        # Additional checks (could include portfolio exposure limits, etc.)
        return int(quantity)