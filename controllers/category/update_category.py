import json

from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash

# Database
from configurations.database import mongo

from flasgger import Swagger 
from flasgger.utils import swag_from

update_category_blueprint = Blueprint("update_category_blueprint", __name__)

@update_category_blueprint.route("/update-category", methods=["PUT"])
@swag_from("update-category_config.yml")
def update_category():
    category = request.json

    category_id = category["category_id"]
    category_id = category_id["$oid"]
    category_name = category["category_name"]
    updated_at = datetime.now()

    mongo.db.category.update_one({
            "_id": ObjectId(category_id),
        },

        {"$set": {
            "category_name": category_name,
            "updated_at": updated_at
        }
    })

    updated_category = mongo.db.category.find_one({"$and": [{"_id": ObjectId(category_id)}, {"record_status": "ACTIVE"}]}, {"password": 0})

    if updated_category:
        updated_category = json.loads(dumps(updated_category))

        return jsonify({
            "status": "200",
            "message": "category_updated_ok",
            "data": updated_category
        })

    else:
        return jsonify({
            "status": "404",
            "message": "category_not_found",
            "data": []
        })