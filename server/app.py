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

# Basic index route
@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

# GET /bakeries route
@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_list = [{
        "id": bakery.id,
        "name": bakery.name,
        "created_at": bakery.created_at.isoformat()
    } for bakery in bakeries]
    
    return make_response(jsonify(bakeries_list), 200)

# GET /bakeries/<int:id> route
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    return make_response(jsonify({
        "id": bakery.id,
        "name": bakery.name,
        "created_at": bakery.created_at.isoformat()
    }), 200)

# GET /baked_goods/by_price route
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [{
        "id": bg.id,
        "name": bg.name,
        "price": bg.price,
        "created_at": bg.created_at.isoformat()
    } for bg in baked_goods]
    
    return make_response(jsonify(baked_goods_list), 200)

# GET /baked_goods/most_expensive route
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive:
        return make_response(jsonify({
            "id": most_expensive.id,
            "name": most_expensive.name,
            "price": most_expensive.price,
            "created_at": most_expensive.created_at.isoformat()
        }), 200)
    else:
        return make_response(jsonify({}), 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
