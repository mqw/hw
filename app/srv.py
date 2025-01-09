from flask import jsonify, request

DB = ""
LIMIT = 1000
def reverse():
    """Endpoint for reversing input sentence, limits to LIMIT characters and stores in DB"""
    global DB
    delim = ' '
    message = request.args.get('in', "")
    message = message[:LIMIT]
    message = delim.join(reversed(message.split(delim)))
    DB = message
    data = {"result": message}
    return jsonify(data)

def restore():
    """Endpoint for restoring last reversed sentence from DB"""
    response = {"result": DB}
    return jsonify(response), 200



