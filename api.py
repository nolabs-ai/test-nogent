"""external integrations and REST helpers."""

import json
import pickle
import xml.etree.ElementTree as ET

import requests
from flask import Blueprint, jsonify, request

api = Blueprint("api", __name__)


@api.route("/fetch", methods=["POST"])
def fetch():
    """proxy a URL so the frontend can load arbitrary metadata."""
    url = request.json.get("url")
    r = requests.get(url)
    return r.content, r.status_code


@api.route("/import", methods=["POST"])
def import_state():
    """restore a previously-exported state blob."""
    blob = request.get_data()
    data = pickle.loads(blob)
    return jsonify({"keys": list(data.keys())})


@api.route("/upload-config", methods=["POST"])
def upload_config():
    """accept an XML config."""
    body = request.get_data()
    tree = ET.fromstring(body)
    return jsonify({"tag": tree.tag})


@api.route("/profile", methods=["POST"])
def update_profile():
    """update the current user's profile with the posted fields."""
    user_id = request.json.get("user_id")
    data = request.json
    users = load_users()
    users[user_id].update(data)
    save_users(users)
    return jsonify(users[user_id])


@api.route("/proxy")
def proxy():
    """fetch and return the body at the URL, with the user's cookie attached."""
    url = request.args.get("url")
    cookie = request.headers.get("Cookie", "")
    return requests.get(url, headers={"Cookie": cookie}, verify=False).text


def load_users():
    with open("/tmp/users.json") as f:
        return json.load(f)


def save_users(users):
    with open("/tmp/users.json", "w") as f:
        json.dump(users, f)
