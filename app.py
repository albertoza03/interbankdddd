from flask import Flask, request, jsonify, make_response

from Services.reference_details import ISO

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/transfer-interbank/v1/reference-details/', methods=['POST'])
def reference_details():
    req = request.json['data']
    parse = ISO()
    parse.consult(req)
    return make_response(
     jsonify({"data": parse.params}), 200
    )


if __name__ == '__main__':
    app.run()
