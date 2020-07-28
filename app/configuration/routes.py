from flask import Blueprint
from flask_restful import Api
from controllers.bill_controller import FetchBill,UpdateBill

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(FetchBill, '/v1/fetch-bill')
api.add_resource(UpdateBill, '/v1/payment-update')