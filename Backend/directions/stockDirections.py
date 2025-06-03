from flask import Blueprint, request, jsonify
import Backend.GlobalInfo.ResponseMessages as ResponseMessages
import Backend.functions.stockFunctions as stockFunctions

stockBP = Blueprint('stockBP', __name__, url_prefix='/api/stock')

@stockBP.get('')
def getStocks():
    try:
        stockData = stockFunctions.getAllStocks()
        print("Stock Data:", stockData) 
        if not stockData:
            return jsonify(ResponseMessages.err472), 472
        # Cast ObjectId to string for JSON serialization
        for stock in stockData:
            if '_id' in stock:
                stock['_id'] = str(stock['_id'])
        return jsonify(ResponseMessages.succ200, stockData), 200
    except Exception as e:
        print(f"Error fetching stocks: {e}")
        return jsonify(ResponseMessages.err500)
    

@stockBP.get('/<name>')
def getStock(name):
    try:
        if not name:
            return jsonify(ResponseMessages.err203)
        stockData = stockFunctions.getStockByName(name)
        print("Stock Data for :", name, stockData)
        if not stockData:
            return jsonify(ResponseMessages.err472)
        # Cast ObjectId to string for JSON serialization
        if '_id' in stockData:
            stockData['_id'] = str(stockData['_id'])
        return jsonify(ResponseMessages.succ200, stockData), 200
    except Exception as e:
        print(f"Error fetching stock {name}: {e}")
        return jsonify(ResponseMessages.err500)
    
@stockBP.post('')
def postStock():
    try:
        requestData = request.get_json()
        if not requestData:
            return jsonify(ResponseMessages.err472)
        
        if 'name' not in requestData or 'cost' not in requestData:
            return jsonify(ResponseMessages.err203)

        print("Request Data for POST Stock:", requestData)
        return stockFunctions.postStock(requestData['name'], requestData['cost'])
    except Exception as e:
        print(f"Error processing POST stock request: {e}")
        return jsonify(ResponseMessages.err500)
    
@stockBP.post('/multiple')
def postMultipleStocks():
    try:
        requestData = request.get_json()
        print("Request Data for POST Multiple Stocks:", requestData)
        if not requestData:
            return jsonify(ResponseMessages.err472)
        
        if not isinstance(requestData, list):
            return jsonify(ResponseMessages.err203)
        if len(requestData) == 0 :
            return jsonify(ResponseMessages.err203)

        return stockFunctions.postMultipleStocks(requestData)
    except Exception as e:
        print(f"Error processing POST multiple stocks request: {e}")
        return jsonify(ResponseMessages.err500)