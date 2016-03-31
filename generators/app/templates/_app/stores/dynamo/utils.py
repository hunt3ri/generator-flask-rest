import boto3
import os
from flask import current_app


def get_config():
    return current_app.config['DYNAMODB_CONFIG']


def initialise_dynamo_connection(config=None):
    """
    Initialise boto resource object appropriately dependent on which environment we're running in
    :param config: Optional config param that allows caller to inject their own config
    :return: Initialised boto resource object that can interact with DynamoDB
    """
    if config is None:
        dynamo_config = get_config()
    else:
        dynamo_config = config

    region_name = str(dynamo_config['region_name']).lower()
    endpoint_url = str(dynamo_config['endpoint_url']).lower()

    # Attempt to get keys from OS
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', None)
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY', None)

    if (aws_access_key_id is None) or (aws_secret_access_key is None):
        raise RuntimeError('AWS Keys have not been set on OS')

    dynamodb = boto3.resource('dynamodb',
                              region_name=region_name,
                              endpoint_url=endpoint_url,
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)

    return dynamodb
