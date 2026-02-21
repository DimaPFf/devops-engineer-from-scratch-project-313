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


def _get_ping():
    return "pong"


def _get_links():
    links = get_all_links()
    return json.jsonify([link.model_dump(mode="json") for link in links])


def _post_links():
    data = request.get_json()
    if data is None:
        return "Bad request", 400
    error = validate_data(data)
    if error:
        return json.jsonify(error), 400
    create_link(
        original_url=data["original_url"],
        short_name=data["short_name"],
    )
    return "Created", 201


def _get_link(id):
    link = get_link_by_id(id)
    if link:
        return json.jsonify(link.model_dump(mode="json"))
    return "Not found", 404


def _delete_link(id):
    if not delete_link(id):
        current_app.logger.info(f"Link {id} not found")
    return "No Content", 204


def _put_link(id):
    data = request.get_json()
    if data is None:
        return "Bad request", 400
    error = validate_data(data)
    if error:
        return json.jsonify(error), 400
    link = update_link(
        id,
        original_url=data["original_url"],
        short_name=data["short_name"],
    )
    if link:
        current_app.logger.info(f"Link updated: {id}")
        return json.jsonify(link.model_dump(mode="json")), 200
    current_app.logger.info(f"Link {id} not found")
    return "Not found", 404


def create_app():
    app = Flask(__name__)
    create_db_and_tables()
    app.get("/ping")(_get_ping)
    app.get("/api/links")(_get_links)
    app.post("/api/links")(_post_links)
    app.get("/api/links/<int:id>")(_get_link)
    app.delete("/api/links/<int:id>")(_delete_link)
    app.put("/api/links/<int:id>")(_put_link)
    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)