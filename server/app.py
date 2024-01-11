#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries', methods=["POST"])
def bakeries():
    if request.method == 'POST':
        # get data from form
        bakery_id = request.form.get("bakery_id")
        name = request.form.get("name")
        price = request.form.get("price")
        # creating new baked goods instance
        new_baked_good = BakedGood(
            bakery_id=bakery_id,
            name=name,
            price=price
        )
        db.session.add(new_baked_good)
        db.session.commit()

        response_data = new_baked_good.to_dict()
        return make_response(response_data, 201)

@app.route('/bakeries/<int:id>', methods=["PATCH"])
def bakery_by_id(id):
    if request.method == "PATCH":
        bakery = Bakery.query.get(id)

        if bakery:
            for attr in request.form:
                setattr(bakery, attr, request.form.get(attr))

            db.session.add(bakery)
            db.session.commit()

            bakery_serialized = bakery.to_dict()
            return make_response(bakery_serialized, 200)
        else:
            response_body = {
                "error": f"Bakery with ID {id} not found."
            }
            return make_response(jsonify(response_body), 404)


@app.route('/baked_goods/<int:id>', methods=["DELETE"])
def bakedGoods_by_id(id):
    if request.method == 'DELETE':
        baked_good = BakedGood.query.get(id)
        if baked_good:
            db.session.delete(baked_good)
            db.session.commit()
            response_body = {
                "deleted_successfuly": True,
                "message": "Deleted."
            }
            return make_response(jsonify(response_body), 200)
        else:
            response_body = {
                "deleted_successfuly": False,
                "message": f"BakedGood with ID {id} not found."
            }
            return make_response(jsonify(response_body), 404)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

if __name__ == '__main__':
    app.run(port=5555, debug=True)