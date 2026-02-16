from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.get("/ping")
    def get_ping():
        return "pong"

    return app


app = create_app()

if __name__ == "__main__":
    app.run()