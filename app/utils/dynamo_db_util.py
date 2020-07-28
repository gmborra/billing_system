import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError, EndpointConnectionError
from .logging_util import logger
from simple_settings import settings


class DynamoDB(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DynamoDB, cls).__new__(cls)
            try:
                db = boto3.resource("dynamodb", region_name=settings.AWS_REGION, endpoint_url=settings.DYNAMODB_HOST)
                cls.customer_bill_details = db.Table(settings.CUSTOMER_BILL_DETAILS)
                cls.transaction_history = db.Table(settings.TRANSACTION_HISTORY)
            except EndpointConnectionError as e:
                logger.error("DynamoDB_ConnectionError = %s", e.message)
                raise e
        return cls._instance

    def fetch_bill_details(self, mobile_number):
        attributes = self.customer_bill_details.query(
            IndexName='mobile_number_index',
            ProjectionExpression='refID,customerName,dueAmount,dueDate',
            KeyConditionExpression=Key('mobileNumber').eq(mobile_number)
        )
        if 'Items' in attributes and len(attributes['Items']) == 1:
            attributes = attributes['Items'][0]

        return attributes

    def get_due_amount(self, ref_id):
        attributes = self.customer_bill_details.query(
            ProjectionExpression='refID,customerName,dueAmount,dueDate',
            KeyConditionExpression=Key('refID').eq(ref_id)
        )
        if 'Items' in attributes and len(attributes['Items']) == 1:
            return  attributes['Items'][0]['dueAmount']

        return 0

    def update_bill_details(self,ref_id,trans_id,amount,date):
        update_exp = "set #due_amount = :due_amount"
        exp_names = {'#due_amount': 'dueAmount'}
        exp_values = {':due_amount': amount}
        response = self.customer_bill_details.update_item(
            Key={'refID': ref_id},
            ConditionExpression="attribute_exists(refID)",
            UpdateExpression=update_exp,
            ExpressionAttributeValues=exp_values,
            ExpressionAttributeNames=exp_names,
            ReturnValues="ALL_NEW"
        )

        self.log_transaction_history(ref_id, trans_id, amount,date)

    def log_transaction_history(self, ref_id, trans_id, amount, date):
        try:
            item = {
                'ref_id': ref_id,
                'trans_id': trans_id,
                'amount': amount,
                'date': date
            }

            self.transaction_history.put_item(Item=item)
        except ClientError as err:
            logger.error("Dynamo_Exception_Put_Transaction_History %s", err.response['Error'])

    def is_duplicate_transaction(self, ref_id, trans_id):
        key = {'ref_id': ref_id, 'trans_id':trans_id}
        response = self.transaction_history.get_item(Key=key)
        if response.get('Item'):
            return  True
        return  False
