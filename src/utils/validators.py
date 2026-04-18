import re
from datetime import datetime

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    pattern = r'^\+?[78][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$'
    return re.match(pattern, phone) is not None

def validate_date(date_string: str) -> bool:
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_amount(amount) -> bool:
    try:
        return float(amount) > 0
    except (ValueError, TypeError):
        return False