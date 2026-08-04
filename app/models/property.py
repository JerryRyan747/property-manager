from app.extensions import db


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    purchase_price = db.Column(db.Float, nullable=False)
    current_value = db.Column(db.Float)
    annual_rent = db.Column(db.Float)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    @property
    def gain_loss(self):
        if self.current_value is None:
            return None
        return self.current_value - self.purchase_price

    def __repr__(self):
        return f"<Property {self.name}>"