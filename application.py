from flask import Flask, request, jsonify, render_template
import logging

logging.basicConfig(level=logging.INFO)

application = Flask(__name__)

secret = "OK"  # can you access this data


@application.route('/', methods=['GET', 'POST'])
def tryme():
    if request.method == 'GET':
        return render_template('try.html')

@application.route("/execute", methods=['GET', 'POST'])
def execute():
    logging.info(f"Received request: {request.method}")
    data = request.get_json(silent=True)
    if data is None:
        logging.warning("Invalid JSON or missing Content-Type header")
        return jsonify({"error": "Invalid JSON or missing Content-Type header"}), 400
    
    code = data.get('code')
    if code is None:
        logging.warning("Missing 'code' in request body")
        return jsonify({"error": "Missing 'code' in request body"}), 400

    logging.info(f"Executing code: {code}")
    response = {}
    try:
        exec(code, {"__builtins__": None}, response)
    except Exception as e:
        logging.error(f"Error executing code: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
    logging.info(f"Execution successful. Response: {response}")
    return jsonify(response)

if __name__ == '__main__':

    application.run()
