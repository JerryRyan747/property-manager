from app.models.property import Property

def portfolio_summary():

    properties = Property.query.all()

    total_properties = len(properties)

    total_value = sum(

        p.purchase_price

        for p in properties

    )

    average_price = (

        total_value / total_properties

        if total_properties

        else 0

    )

    latest = (

        properties[-1].name

        if properties

        else "None"

    )

    return {

        "total_properties": total_properties,

        "total_value": total_value,

        "average_price": average_price,

        "latest": latest

    }