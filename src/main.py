from datetime import datetime
import os
import re

from flask import Flask, json, logging, request
from sqlmodel import select, update

from .database.connect_db import create_db_and_tables, get_session
from .database.model_link import Link
from .utils.make_short_url import make_short_url
from .utils.validators import validate_data


def create_app():
    app = Flask(__name__)
    create_db_and_tables()

    @app.get("/ping")
    def get_ping():
        return "pong"

    @app.get("/api/links")
    def get_links():
        with get_session() as session:
            links = session.exec(select(Link)).all()
            return json.jsonify([link.model_dump(mode="json") for link in links])

    @app.post("/api/links")
    def create_links():
        data = request.get_json()
        if data is None:
            return "Bad request", 400
        error = validate_data(data)
        if error:
            return json.jsonify(error), 400
        with get_session() as session:
            link = Link(original_url=data['original_url'], short_name=data['short_name'], short_url=make_short_url(data['short_name']))
            session.add(link)
            session.commit()
            session.refresh(link)
            return 'Created', 201

    @app.get("/api/links/<int:id>")
    def get_links_by_id(id):
        with get_session() as session:
            link = session.get(Link, id)
            if link:
                return json.jsonify(link.model_dump(mode="json"))
            return 'Not found', 404

    @app.delete("/api/links/<int:id>")
    def delete_links(id):
        with get_session() as session:
            link = session.get(Link, id)
            if link:
                session.delete(link)
                session.commit()
                return "No Content", 204
            else:
                app.logger.info(f"Link {id} not found")
                return "No Content", 204

    @app.put("/api/links/<int:id>")
    def update_links(id):
        data = request.get_json()
        if data is None:
            return "Bad request", 400
        error = validate_data(data)
        if error:
            return json.jsonify(error), 400
        with get_session() as session:
            link = session.get(Link, id)
            
            if link:
                link.original_url=data['original_url'],
                link.short_name=data['short_name'],
                link.short_url=make_short_url(data['short_name']),
                link.updated_at = datetime.now()
                
                session.add(link)
                session.commit()
                session.refresh(link)
                
                app.logger.info(f"Link updated: {id}")
                return link.model_dump(mode="json"), 200
            else:
                app.logger.info(f"User {id} not found")
                return 'Not found', 404

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)