import secrets

from flask import Flask, request, jsonify, make_response

from utils.generate_trx import GenerateTrx
from Services.reference_details import ISO

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/transfer-interbank/v1/reference-details', methods=['POST'])
def reference_details():
    req: dict = request.json
    req: str = req.get('data', '')
    if req:
        parse = ISO()
        parse.consult(req)
        return make_response(
         jsonify({"data": parse.params}), 200
        )

    return make_response(
         jsonify({"message": "", "code": ""}), 400
        )


@app.route('/transfer-core-banks/v1/transaction', methods=['GET'])
def generate_trx():
    generate = GenerateTrx()
    trx = generate.generate()
    return make_response(
     jsonify(trx), 201
    )


@app.route('/transfer/v1/tokens', methods=['POST'])
def generate_token():
    return make_response(
     jsonify({"token": secrets.token_hex(16)}), 201
    )


@app.route('/transfer/v1/init', methods=['POST'])
def generate_transfer():
    return make_response(jsonify(), 201)


if __name__ == '__main__':
    app.run()
