from datetime import date
from decimal import Decimal
from ..database.connection import db
from ..utils.exceptions import NotFoundError, ValidationError

class PaymentService:
    
    def create_payment(self, amount: Decimal, method: str, id_subscription: int):
        if method not in ('СБП', 'Карта'):
            raise ValidationError("Invalid payment method")
        
        if amount <= 0:
            raise ValidationError("Amount must be positive")
        
        subscription = db.execute_query(
            "SELECT ID_Subscription FROM Subscriptions WHERE ID_Subscription = %s",
            (id_subscription,), fetch_one=True
        )
        if not subscription:
            raise NotFoundError(f"Subscription {id_subscription} not found")
        
        result = db.execute_query(
            """
            INSERT INTO Payments (Amount, Date, Method, ID_Subscription)
            VALUES (%s, %s, %s, %s)
            RETURNING ID_Payment
            """,
            (amount, date.today(), method, id_subscription),
            fetch_one=True)
