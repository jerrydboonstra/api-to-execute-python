from flask import Flask, request, jsonify, render_template
import logging
import io
from contextlib import redirect_stdout

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
    output = io.StringIO()
    safe_builtins = {
        'abs': abs, 'all': all, 'any': any, 'bin': bin,
        'bool': bool, 'chr': chr, 'dict': dict, 'float': float,
        'int': int, 'len': len, 'list': list, 'max': max,
        'min': min, 'ord': ord, 'pow': pow, 'range': range,
        'round': round, 'set': set, 'str': str, 'sum': sum,
        'tuple': tuple, 'type': type, 'print': print
    }
    try:
        with redirect_stdout(output):
            exec(code, {"__builtins__": safe_builtins}, response)
    except Exception as e:
        logging.error(f"Error executing code: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
    response['output'] = output.getvalue()
    logging.info(f"Execution successful. Response: {response}")
    return jsonify(response)

if __name__ == '__main__':

    application.run()
