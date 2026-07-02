from flask import Blueprint, render_template, request, redirect, url_for


from app.extensions import db


from app.models.property import Property


from app.services.portfolio import portfolio_summary


main = Blueprint("main", __name__)


@main.route("/")


def home():


    properties = Property.query.order_by(Property.name).all()


    summary = portfolio_summary()


    return render_template(


        "home.html",


        properties=properties,


        summary=summary


    )


@main.route("/add-property", methods=["POST"])


def add_property():


    property = Property(


        name=request.form["name"],


        address=request.form["address"],


        purchase_price=float(request.form["purchase_price"])


    )


    db.session.add(property)


    db.session.commit()


    return redirect(url_for("main.home"))