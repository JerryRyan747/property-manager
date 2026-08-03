from app.models.property import Property

def portfolio_summary():

    properties = Property.query.all()

    total_properties = len(properties)

    total_purchase = sum(p.purchase_price for p in properties)

    total_current = sum(

        p.current_value if p.current_value else p.purchase_price

        for p in properties

    )

    total_gain = total_current - total_purchase

    average_price = (

        total_purchase / total_properties

        if total_properties else 0

    )

    latest = properties[-1].name if properties else "None"

    return {

        "total_properties": total_properties,

        "total_purchase": total_purchase,

        "total_current": total_current,

        "total_gain": total_gain,

        "average_price": average_price,

        "latest": latest

    }