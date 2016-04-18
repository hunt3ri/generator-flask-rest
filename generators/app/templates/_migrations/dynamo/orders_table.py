from app.stores.dynamo.utils import initialise_dynamo_connection
from botocore.exceptions import ClientError


def create_orders_table(table_name, logger, dynamo_config):
    """
    Creates a table in Dynamo in the format map_store.environment.orders
    :param table_name: Table we want to create
    :param logger: Logger object
    :param dynamo_config: Dynamo Config for connection
    """

    dynamodb = initialise_dynamo_connection(dynamo_config)
    orders_table = dynamodb.Table(table_name)

    # Don't create table if it already exists
    try:
        status = orders_table.table_status
        logger.debug('Table {0} exists, status is {1}'.format(table_name, status))
        return
    except ClientError:
        # Swallow this exception as it demonstrates table doesn't exist
        pass

    logger.info('Creating table {0}'.format(table_name))
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'customerEmailAddress',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'orderId',
                'KeyType': 'RANGE'  # Sort Key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'customerEmailAddress',
                'AttributeType': 'S'  # String
            },
            {
                'AttributeName': 'orderId',
                'AttributeType': 'S'  # String
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    logger.info('Table {0} created'.format(table_name))
