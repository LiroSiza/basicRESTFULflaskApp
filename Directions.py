from Backend.app import app
from Backend.directions.stockDirections import stockBP

app.register_blueprint(stockBP)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9005 ,debug=True)