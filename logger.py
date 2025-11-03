import gspread
from datetime import datetime

class SheetsLogger:
    def __init__(self, creds_file: str, doc_name: str):
        self.gc = gspread.service_account(filename=creds_file)
        self.sheet = self.gc.open(doc_name).sheet1

    def log_trade(self, symbol, side, quantity, price, stop, target, reason):
        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            symbol, side, quantity, price, stop, target, reason
        ]
        try:
            self.sheet.append_row(row)
        except Exception as e:
            print(f"[Logger] Failed to log to Google Sheets: {e}")