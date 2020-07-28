import os
PROJECT_BASE_PATH = os.path.dirname(__file__)
PROJECT_BASE_PATH = os.path.join(PROJECT_BASE_PATH, '../')
PORT = 5555
AWS_REGION = "aws-dev"
DYNAMODB_HOST = "http://localhost:8000/"
CUSTOMER_BILL_DETAILS = "customer_bill_details" # should be two separate tables ?
TRANSACTION_HISTORY = "transaction_history"
