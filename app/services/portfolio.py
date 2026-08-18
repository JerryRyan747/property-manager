from collections import defaultdict
from app.models.property import Property
from datetime import datetime

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

    total_expenses = sum(
    p.annual_expenses or 0
    for p in properties
    )

    total_net_cash_flow = (
    total_net_rental_income - total_expenses
    )

    current_year = datetime.now().year
    maturity_by_year = defaultdict(float)

    for p in properties:
        if p.mortgage_balance and p.mortgage_maturity_year:
            maturity_by_year[p.mortgage_maturity_year] += p.mortgage_balance

    refinancing_exposure_5yr = sum(
    amount
    for year, amount in maturity_by_year.items()
        if year <= current_year + 5
    )

    refinancing_exposure_5yr_pct = (
    refinancing_exposure_5yr / total_mortgage * 100
    if total_mortgage
    else 0
    )

    net_yield = (
        (total_net_rental_income / total_current) * 100
        if total_current else 0
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

        "net_yield": net_yield,

        "total_expenses": total_expenses,

        "total_net_cash_flow": total_net_cash_flow,

        "maturity_by_year": dict(sorted(maturity_by_year.items())),

        "current_year": current_year,

        "refinancing_exposure_5yr": refinancing_exposure_5yr,

        "refinancing_exposure_5yr_pct": refinancing_exposure_5yr_pct,

        "latest": latest

        

    }