#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = Bakery.query.all()
    return [bakery.to_dict() for bakery in all_bakeries]

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery:
        return bakery.to_dict()
    else:
        return jsonify({"error": "Bakery not found"}), 404

@app.route('/baked_goods/by_price') #sorted by price in descending order
def baked_goods_by_price():
    return [baked_good.to_dict() for baked_good in BakedGood.query.order_by(BakedGood.price.desc()).all()]

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive:
        return most_expensive.to_dict()
    else:
        return jsonify({"error": "No baked goods found"}), 404
if __name__ == '__main__':
    app.run(port=5555, debug=True)
