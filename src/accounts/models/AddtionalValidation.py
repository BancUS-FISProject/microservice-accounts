import re
from schwifty import IBAN
from schwifty.exceptions import SchwiftyException


def validate_email(email: str) -> bool:
    patron = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'
    if re.match(patron, email):
        return True
    else:
        return False
    
def validate_subscription(subscription: str) -> bool:
    subscriptions = ["Free"]
    
    if subscription in subscriptions:
        return True
    else:
        return False
    
def validate_iban(iban: str) -> bool:
    try:
        IBAN(iban)
        return True
    except SchwiftyException:
        return False