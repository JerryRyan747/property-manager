from app.extensions import db


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    purchase_price = db.Column(db.Float, nullable=False)
    current_value = db.Column(db.Float)
    annual_rent = db.Column(db.Float)
    annual_expenses = db.Column(db.Float)
    mortgage_balance = db.Column(db.Float)
    interest_rate = db.Column(db.Float)
    mortgage_term = db.Column(db.Integer)
    mortgage_type = db.Column(
    db.String(20),
    default="interest_only"
    )

    @property
    def mortgage_maturity_year(self):
        if self.mortgage_term is None:
            return None

        from datetime import datetime

        return datetime.now().year + self.mortgage_term

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    @property
    def gain_loss(self):
        if self.current_value is None:
            return None
        return self.current_value - self.purchase_price

    @property
    def annual_interest_cost(self):
        if not self.mortgage_balance or not self.interest_rate:
            return 0

        return (
            self.mortgage_balance *
            self.interest_rate / 100
        )

    @property
    def monthly_mortgage_payment(self):
        if (
            self.mortgage_type != "repayment"
            or not self.mortgage_balance
            or self.interest_rate is None
            or self.mortgage_term is None
            or self.mortgage_term <= 0
        ):
            return 0

        monthly_rate = self.interest_rate / 100 / 12
        number_of_payments = self.mortgage_term * 12

        if monthly_rate == 0:
            return self.mortgage_balance / number_of_payments

        return (
            self.mortgage_balance
            * monthly_rate
            * (1 + monthly_rate) ** number_of_payments
            / ((1 + monthly_rate) ** number_of_payments - 1)
        )

    @property
    def annual_mortgage_payment(self):
        if self.mortgage_type == "repayment":
            return self.monthly_mortgage_payment * 12

        return self.annual_interest_cost

    @property
    def annual_principal_repayment(self):
        if self.mortgage_type != "repayment":
            return 0

        principal = (
        self.annual_mortgage_payment
        - self.annual_interest_cost
)

        return max(principal, 0)
 
    @property
    def net_rental_income(self):
        if not self.annual_rent:
            return 0

        return self.annual_rent - self.annual_interest_cost

    @property
    def net_cash_flow(self):
        if not self.annual_rent:
            return 0

        return (
            self.annual_rent
            - self.annual_mortgage_payment
            - (self.annual_expenses or 0)
            )

    
    @property
    def cash_flow_yield(self):
        if not self.current_value:
            return 0

        return (
            self.net_cash_flow
            / self.current_value
            * 100
        )

    @property
    def ltv(self):
        if not self.mortgage_balance or not self.current_value:
            return None

        return (
            self.mortgage_balance /
            self.current_value * 100
        )

    def __repr__(self):
        return f"<Property {self.name}>"