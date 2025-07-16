# app.py
from flask import Flask
from backend.routes import bp as dns_routes

app = Flask(__name__)
app.register_blueprint(dns_routes, url_prefix="/api")

@app.route("/")
def root():
    return "✅ DNS Insight Backend running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
