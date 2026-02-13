from flask import Flask

app = Flask(__name__)

@app.get("/ping")
def get_ping():
    return "pong"

if __name__ == "__main__":
    app.run(port=8080, debug=True)