from flask import make_response, jsonify

# Jsonifies the passed object, and makes a response object out of it
def sendResponse(result):
    resp = make_response(jsonify(result))
    resp.mimetype = 'application/json'
    return resp
