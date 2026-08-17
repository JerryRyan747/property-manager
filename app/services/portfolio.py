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
    total_mortgage = sum(
        p.mortgage_balance or 0
        for p in properties
    )

    total_equity = (
        total_current - total_mortgage
    )
    total_annual_rent = sum(
    p.annual_rent if p.annual_rent else 0
    for p in properties
    )

    total_interest = sum(
    p.annual_interest_cost
    for p in properties
    )

    total_net_rental_income = (
    total_annual_rent - total_interest
    )

    average_yield = (
    (total_annual_rent / total_current) * 100
    if total_current else 0
    )

    total_mortgage = sum(
    p.mortgage_balance if p.mortgage_balance else 0
    for p in properties
    )

    total_equity = total_current - total_mortgage

    portfolio_ltv = (
    (total_mortgage / total_current) * 100
    if total_current else 0
    )

    
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

        "total_annual_rent": total_annual_rent,

        "average_price": average_price,

        "average_yield": average_yield,

        "total_mortgage": total_mortgage,

        "total_equity": total_equity,

        "portfolio_ltv": portfolio_ltv,

        "total_mortgage": total_mortgage,

        "total_equity": total_equity,

        "total_interest": total_interest,
        
        "total_net_rental_income": total_net_rental_income,

        "latest": latest

        

    }