import os

from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.get("/ping")
    def get_ping():
        return "pong"

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)