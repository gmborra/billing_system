from flask_cors import CORS
from flask import g, request, json, Response, Flask, jsonify

from configuration.config import create_app
from simple_settings import settings

app = create_app()

cors = CORS(app)

@app.before_request
def authenticate_request():
    pass


@app.after_request
def allow_origin(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
    return response


@app.errorhandler(404)
def page_not_found(e):
    return Response(
        response=json.dumps({"error": "NOT FOUND", "status_code": 404}),
        status=404,
        mimetype='application/json')


@app.errorhandler(Exception)
def handle_audit_exception(error):
    response = jsonify(error.data)
    response.status_code = error.status_code
    return response


if __name__ == "__main__":
    app.run(host="localhost", port=settings.PORT)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()