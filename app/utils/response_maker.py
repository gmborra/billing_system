import decimal
from flask import Response, json
from utils.status_codes import status_codes


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class MakeResponse(object):
    # json.dumps(response_object)
    @staticmethod
    def send_response(response_object, status_code=200):
        return Response(response=json.dumps(response_object),
                        status=status_code,
                        mimetype='application/json')

    @staticmethod
    def success(response_object):
        data = {'data': response_object,'status':'SUCCESS'}
        return MakeResponse.send_response(
            data, 200)


    @staticmethod
    def error(error_code):
        error = {"errorCode":error_code,"status": "ERROR"}
        return MakeResponse.send_response(
            error, status_codes.get(error_code, 500))