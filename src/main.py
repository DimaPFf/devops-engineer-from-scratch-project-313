import os

from flask import Flask, current_app, json, request

from src.database.connect_db import create_db_and_tables
from src.services.link_service import (
    create_link,
    delete_link,
    get_all_links,
    get_link_by_id,
    update_link,
)
from src.utils.validators import validate_data

app = Flask(__name__)

if os.getenv("PYTEST_CURRENT_TEST") is None:
    create_db_and_tables()


@app.get("/ping")
def get_ping():
    return "pong"


@app.get("/api/links")
def get_links():
    links = get_all_links()
    return json.jsonify([link.model_dump(mode="json") for link in links])


@app.post("/api/links")
def post_links():
    data = request.get_json()
    if data is None:
        return json.jsonify({"error": "Bad request"}), 400
    error = validate_data(data)
    if error:
        return json.jsonify(error), 400
    link = create_link(
        original_url=data["original_url"],
        short_name=data["short_name"],
    )
    return json.jsonify(link.model_dump(mode="json")), 201


@app.get("/api/links/<int:link_id>")
def get_link(link_id):
    link = get_link_by_id(link_id)
    if link:
        return json.jsonify(link.model_dump(mode="json"))
    return json.jsonify({"error": "Not found"}), 404


@app.delete("/api/links/<int:link_id>")
def delete_link_route(link_id):
    if not delete_link(link_id):
        current_app.logger.info("Link %s not found", link_id)
    return "", 204


@app.put("/api/links/<int:link_id>")
def put_link(link_id):
    data = request.get_json()
    if data is None:
        return json.jsonify({"error": "Bad request"}), 400
    error = validate_data(data)
    if error:
        return json.jsonify(error), 400
    link = update_link(
        link_id,
        original_url=data["original_url"],
        short_name=data["short_name"],
    )
    if link:
        current_app.logger.info("Link updated: %s", link_id)
        return json.jsonify(link.model_dump(mode="json")), 200
    current_app.logger.info("Link %s not found", link_id)
    return json.jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)