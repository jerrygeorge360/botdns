# app.py
from flask import Flask
from routes import bp as dns_routes

app = Flask(__name__)
app.register_blueprint(dns_routes, url_prefix="/api")

@app.route("/")
def root():
    return "✅ DNS Insight Backend running."

if __name__ == "__main__":
    app.run(port=5001,debug=True)
