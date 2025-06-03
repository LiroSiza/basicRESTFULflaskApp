from flask import jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import Backend.GlobalInfo.Keys as Keys
import Backend.GlobalInfo.ResponseMessages as ResponseMessages

# Initialize MongoDB connection if not already done - No Auth
if Keys.dbconn == None:
    mongoConnection = MongoClient(Keys.strConnection)   # Client
    Keys.dbconn = mongoConnection[Keys.strDBConnection] # Database
    dbConnStocks = Keys.dbconn['stocks']                # Collection


def getAllStocks():
    try:
        response = dbConnStocks.find()  # Fetch all stock documents
        print("Response from DB:", response)
        if response is None:
            return ResponseMessages.err203
        #objResponse = ResponseMessages.succ200.copy()
        #objResponse['stocks'] = list(response)  # Convert cursor to list
        #return objResponse
        return list(response)  # Convert cursor to list
    except Exception as e:
        print(f"Error fetching stocks: {e}")
        return None
    
def getStockByName(name):
    try:
        response = dbConnStocks.find_one({"name" : name})
        print("Response from DB:", response)
        if response is None:
            return ResponseMessages.err203
        #objResponse = ResponseMessages.succ200.copy()
        #objResponse['stocks'] = list(response)  # Convert cursor to list
        #return objResponse
        return response
    except Exception as e:
        print(f"Error fetching stock {name}: {e}")
        return None
    
def postStock(name, cost):
    try:
        if not name or not cost:
            return ResponseMessages.err203
        
        result = dbConnStocks.insert_one({"name": name,"cost": cost})
        print("Inserted Stock ID:", result.inserted_id)

        response = ResponseMessages.succ200.copy()
        response['stock_id'] = str(result.inserted_id)
        return response
    except Exception as e:
        print(f"Error inserting stock {name}: {e}")
        return jsonify(ResponseMessages.err500)
    
def postMultipleStocks(stocks):
    try:
        for stock in stocks:
            print("Stock:", stock )
        
        response = dbConnStocks.insert_many(stocks)

        response = ResponseMessages.succ200.copy()
        response['Saved'] = True
        return response
    except Exception as e:
        print(f"Error inserting multiple stocks: {e}")
        return jsonify(ResponseMessages.err500)