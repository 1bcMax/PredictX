from decimal import Decimal

def calculate_accuracy(predicted: Decimal, actual: Decimal) -> float:
    """Calculate prediction accuracy."""
    return 1 - abs(predicted - actual) / actual

def format_price(price: Decimal) -> str:
    """Format price with appropriate decimals."""
    return f"${price:,.2f}"
