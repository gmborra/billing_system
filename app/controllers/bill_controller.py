from flask import request, json
from flask_restful import Resource
from utils import logger,DynamoDB,MakeResponse
import uuid


class FetchBill(Resource):
    @staticmethod
    def post(*args, **kwargs):
        try:
            """fetch the bill details"""
            req_json = json.loads(request.data)
            logger.info("fetch_bill_details_input={}".format(req_json))
            mobile_number = req_json['mobileNumber']
            response = DynamoDB().fetch_bill_details(mobile_number)
            logger.info(response)
            return MakeResponse.success(response)
        except KeyError as err:
            return MakeResponse.error('invalid-api-parameters')
        except Exception as err:
            return MakeResponse.error('Something went wrong!!')


class UpdateBill(Resource):
    @staticmethod
    def post(*args, **kwargs):
        """update the bill details"""
        try:
            req_json = json.loads(request.data)
            logger.info("req_to_update_bill_details_req={}".format(req_json))
            ref_id = req_json['refID']
            trans_id = req_json['transaction']['id']
            amount = req_json['transaction']['amountPaid']
            date =  req_json['transaction']['date']

            if DynamoDB().is_duplicate_transaction(ref_id, trans_id):
                return MakeResponse.success('no need process return')

            due_amount = DynamoDB().get_due_amount(ref_id)
            if due_amount == 0:
                return MakeResponse.success('no amount is due')

            new_due = int(due_amount) - int(amount)

            DynamoDB().update_bill_details(ref_id, trans_id, new_due, date)

            return MakeResponse.success({'ackID':uuid.uuid4()})

        except KeyError as err:
            return MakeResponse.error('invalid-api-parameters')

        except Exception as err:
            print(err)
            return MakeResponse.error('something wrong')