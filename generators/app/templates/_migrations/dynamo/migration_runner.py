from migrations.dynamo.customers_table import create_customers_table
from migrations.dynamo.orders_table import create_orders_table


def run(environment, logger, dynamo_config):
    """
    Run all migrations necessary to set-up AWS Dynamo for the current environment
    :param environment: The current environment, eg Dev, Staging etc
    :param logger: Logger object, this is passed to avoid circular dependencies
    :param dynamo_config: Config needs to be passed as app_context not yet available to the full app
    """
    customer_table_name = str('map_store.' + environment + '.' + 'customers').lower()
    orders_table_name = str('map_store.' + environment + '.' + 'orders').lower()

    create_customers_table(customer_table_name, logger, dynamo_config)
    create_orders_table(orders_table_name, logger, dynamo_config)
