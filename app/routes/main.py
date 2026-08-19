from flask import Blueprint, render_template, request, redirect, url_for, flash


from app.extensions import db


from app.models.property import Property


from app.services.portfolio import portfolio_summary


main = Blueprint("main", __name__)


@main.route("/")

def home():

    search = request.args.get("search", "")

    query = Property.query

    if search:

        query = query.filter(

            (Property.name.contains(search)) |

            (Property.address.contains(search))

        )

    properties = query.order_by(Property.name).all()

    summary = portfolio_summary()

    return render_template(

        "home.html",

        properties=properties,

        summary=summary

    )
@main.route("/property/<int:property_id>")

def property_detail(property_id):

    property = Property.query.get_or_404(property_id)
    summary = portfolio_summary()

    return render_template(

        "property_detail.html",

        property=property,
        summary=summary

    )

@main.route("/add-property", methods=["POST"])

def add_property():

    current_value = request.form.get("current_value")
    annual_rent = request.form.get("annual_rent")
    annual_expenses = request.form.get("annual_expenses")
    mortgage_balance = request.form.get("mortgage_balance")
    interest_rate = request.form.get("interest_rate")
    mortgage_type = request.form.get("mortgage_type")
    mortgage_term = request.form.get("mortgage_term")

    property = Property(

        name=request.form["name"],

        address=request.form["address"],

        purchase_price=float(request.form["purchase_price"]),

        current_value=float(current_value) if current_value else None,

        annual_rent=float(annual_rent) if annual_rent else None,

        annual_expenses=float(annual_expenses) if annual_expenses else None,

        mortgage_balance=float(mortgage_balance) if mortgage_balance else None,

        interest_rate=float(interest_rate) if interest_rate else None,

        mortgage_term=int(mortgage_term) if mortgage_term else None,

        mortgage_type=mortgage_type
    )

    db.session.add(property)

    db.session.commit()
    flash("Property added successfully!", "success")

    return redirect(url_for("main.home"))
    

@main.route("/property/<int:property_id>/edit", methods=["GET", "POST"])


def edit_property(property_id):


    property = Property.query.get_or_404(property_id)


    if request.method == "POST":


        property.name = request.form["name"]


        property.address = request.form["address"]


        property.purchase_price = float(request.form["purchase_price"])


        current_value = request.form.get("current_value")
        annual_rent = request.form.get("annual_rent")
        mortgage_balance = request.form.get("mortgage_balance")
        interest_rate = request.form.get("interest_rate")
        annual_expenses = request.form.get("annual_expenses")
        mortgage_type = request.form.get("mortgage_type")
        mortgage_term = request.form.get("mortgage_term")

        property.current_value = float(current_value) if current_value else None
        property.annual_rent = float(annual_rent) if annual_rent else None
        property.annual_expenses=float(annual_expenses) if annual_expenses else None
        property.mortgage_balance = float(mortgage_balance) if mortgage_balance else None
        property.interest_rate = float(interest_rate) if interest_rate else None
        property.mortgage_term = int(mortgage_term) if mortgage_term else None
        property.mortgage_type = mortgage_type

        
        db.session.commit()
        flash("Property updated successfully!", "success")

        return redirect(url_for("main.home"))


    return render_template(


        "edit_property.html",


        property=property

    )


@main.route("/property/<int:property_id>/delete")

def delete_property(property_id):

    property = Property.query.get_or_404(property_id)

    db.session.delete(property)

    db.session.commit()
    flash("Property deleted successfully!", "success")
    return redirect(url_for("main.home"))


    