from flask import Flask, request, jsonify

app = Flask(__name__)

# To handle GET
@app.route('/', methods=['GET'])
def get():
    return 'Hello, World!'

# To handle POST 
@app.route('/', methods=['POST'])
def post():
    data = request.get_json()
    name = data.get('name')
    if name  and request.method == 'POST':
        resp = jsonify(f'Hello, {name}!')
        resp.status_code = 200
        return resp


# Main function app call
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)