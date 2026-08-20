from collections import defaultdict
from app.models.property import Property
from datetime import datetime

def portfolio_summary():

    properties = Property.query.all()

    total_properties = len(properties)

    total_purchase = sum(
        p.purchase_price for p in properties
    )

    total_current = sum(
        p.current_value if p.current_value else p.purchase_price
        for p in properties
    )

    total_gain = total_current - total_purchase

    total_mortgage = sum(
        p.mortgage_balance or 0
        for p in properties
    )

    total_equity = total_current - total_mortgage

    total_annual_rent = sum(
        p.annual_rent if p.annual_rent else 0
        for p in properties
    )

    total_interest = sum(
        p.annual_interest_cost
        for p in properties
    )

    total_principal_repayment = sum(
        p.annual_principal_repayment
        for p in properties
    )

    total_mortgage_payments = sum(
        p.annual_mortgage_payment
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
        total_annual_rent
        - total_expenses
        - total_mortgage_payments
    )

    current_year = datetime.now().year

    maturity_by_year = defaultdict(float)

    for p in properties:

        if p.mortgage_balance and p.mortgage_maturity_year:

            maturity_by_year[p.mortgage_maturity_year] += (
                p.mortgage_balance
            )

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
        if total_current
        else 0
    )

    average_yield = (
        (total_annual_rent / total_current) * 100
        if total_current
        else 0
    )

    portfolio_ltv = (
        (total_mortgage / total_current) * 100
        if total_current
        else 0
    )

    average_price = (
        total_purchase / total_properties
        if total_properties
        else 0
    )

    # ---------------------------------------------------------
    # Portfolio debt forecast
    # ---------------------------------------------------------

    debt_forecast = []

    forecast_balances = {
        p.id: (p.mortgage_balance or 0)
        for p in properties
    }

    forecast_years = 15

    for year_number in range(1, forecast_years + 1):

        opening_debt = sum(
            forecast_balances.values()
        )

        annual_interest = 0
        annual_principal = 0
        annual_payments = 0

        for p in properties:

            balance = forecast_balances[p.id]

            if not balance:
                continue

            # Interest Only mortgage
            if p.mortgage_type != "repayment":

                interest = (
                    balance
                    * (p.interest_rate or 0)
                    / 100
                )

                principal = 0

                payment = interest

            # Repayment mortgage
            else:

                schedule = p.amortisation_schedule()

                if year_number <= len(schedule):

                    year_data = schedule[year_number - 1]

                    interest = year_data["interest"]

                    principal = year_data["principal"]

                    payment = interest + principal

                else:

                    interest = 0

                    principal = 0

                    payment = 0

            annual_interest += interest

            annual_principal += principal

            annual_payments += payment

            # Reduce outstanding balance
            forecast_balances[p.id] = max(
                balance - principal,
                0
            )

        closing_debt = sum(
            forecast_balances.values()
        )

        # Portfolio equity forecast
        forecast_equity = (
            total_current - closing_debt
        )

        debt_forecast.append({

            "year": current_year + year_number - 1,

            "opening_debt": opening_debt,

            "interest": annual_interest,

            "principal": annual_principal,

            "payments": annual_payments,

            "closing_debt": closing_debt,

            "equity": forecast_equity

        })

    # ---------------------------------------------------------
    # Latest property
    # ---------------------------------------------------------

    latest = (
        properties[-1].name
        if properties
        else "None"
    )

    # ---------------------------------------------------------
    # Return portfolio summary
    # ---------------------------------------------------------

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

        "total_interest": total_interest,

        "total_principal_repayment": total_principal_repayment,

        "total_mortgage_payments": total_mortgage_payments,

        "total_net_rental_income": total_net_rental_income,

        "net_yield": net_yield,

        "total_expenses": total_expenses,

        "total_net_cash_flow": total_net_cash_flow,

        "maturity_by_year": dict(
            sorted(maturity_by_year.items())
        ),

        "current_year": current_year,

        "refinancing_exposure_5yr": refinancing_exposure_5yr,

        "refinancing_exposure_5yr_pct": refinancing_exposure_5yr_pct,

        "debt_forecast": debt_forecast,

        "latest": latest

    }