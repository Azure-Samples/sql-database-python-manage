import os
from haikunator import Haikunator
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.sql import SqlManagementClient

REGION = 'westus'
GROUP_NAME = 'azure-sample-group'
SERVER_NAME = Haikunator().haikunate()
DATABASE_NAME = 'sample-db'

# This script expects that the following environment vars are set:
#
# AZURE_TENANT_ID: with your Azure Active Directory tenant id or domain
# AZURE_CLIENT_ID: with your Azure Active Directory Application Client ID
# AZURE_CLIENT_SECRET: with your Azure Active Directory Application Secret
# AZURE_SUBSCRIPTION_ID: with your Azure Subscription Id
#


def run_example():
    """Storage management example."""
    #
    # Create the Resource Manager Client with an Application (service principal) token provider
    #
    subscription_id = os.environ.get(
        'AZURE_SUBSCRIPTION_ID',
        '11111111-1111-1111-1111-111111111111')  # your Azure Subscription Id
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )
    resource_client = ResourceManagementClient(credentials, subscription_id)
    sql_client = SqlManagementClient(credentials, subscription_id)

    # You MIGHT need to add SQL as a valid provider for these credentials
    # If so, this operation has to be done only once for each credentials
    resource_client.providers.register('Microsoft.Sql')

    # Create Resource group
    print('Create Resource Group')
    resource_group_params = {'location': 'westus'}
    print_item(resource_client.resource_groups.create_or_update(
        GROUP_NAME, resource_group_params))

    # Create a SQL server
    print('Create a SQL server')
    server = sql_client.servers.create_or_update(
        GROUP_NAME,
        SERVER_NAME,
        {
            'location': REGION,
            'version': '12.0',  # Required for create
            'administrator_login': 'mysecretname',  # Required for create
            'administrator_login_password': 'HusH_Sec4et'  # Required for create
        }
    )
    print_item(server)
    print('\n\n')

    # Open access to this server for IPs
    print("Add firewall rule")
    firewall_rule = sql_client.firewall_rules.create_or_update(
        GROUP_NAME,
        SERVER_NAME,
        "firewall_rule_name_123.123.123.123",
        "123.123.123.123",  # Start ip range
        "123.123.123.123"  # End ip range
    )
    print_item(firewall_rule)

    # Get SQL server
    print('Get SQL server')
    server = sql_client.servers.get_by_resource_group(
        GROUP_NAME,
        SERVER_NAME,
    )
    print_item(server)
    print("\n\n")

    # List SQL servers by resource group
    print('List SQL servers in a resource group')
    for item in sql_client.servers.list_by_resource_group(GROUP_NAME):
        print_item(item)
    print("\n\n")

    # List SQL servers by subscription
    print('List SQL servers in a subscription')
    for item in sql_client.servers.list():
        print_item(item)
    print("\n\n")

    # List SQL servers usage
    print('List SQL servers usage')
    for item in sql_client.servers.list_usages(GROUP_NAME, SERVER_NAME):
        print_metric(item)
    print("\n\n")

    # Create a database
    print('Create SQL database')
    async_db_create = sql_client.databases.create_or_update(
        GROUP_NAME,
        SERVER_NAME,
        DATABASE_NAME,
        {
            'location': REGION
        }
    )
    # Wait for completion and return created object
    database = async_db_create.result()
    print_item(database)
    print("\n\n")

    # Get SQL database
    print('Get SQL database')
    database = sql_client.databases.get(
        GROUP_NAME,
        SERVER_NAME,
        DATABASE_NAME
    )
    print_item(database)
    print("\n\n")

    # List SQL databases by server
    print('List SQL databases in a server')
    for item in sql_client.databases.list_by_server(GROUP_NAME, SERVER_NAME):
        print_item(item)
    print("\n\n")

    # List SQL database usage
    print('List SQL database usage')
    for item in sql_client.databases.list_usages(GROUP_NAME, SERVER_NAME, DATABASE_NAME):
        print_metric(item)
    print("\n\n")

    # Delete the SQL databse
    print('Delete the SQL databse')
    sql_client.databases.delete(GROUP_NAME, SERVER_NAME, DATABASE_NAME)
    print("Deleted: {}".format(DATABASE_NAME))
    print("\n\n")

    # Delete the SQL server
    print('Delete the SQL server')
    sql_client.servers.delete(GROUP_NAME, SERVER_NAME)
    print("Deleted: {}".format(SERVER_NAME))
    print("\n\n")

    # Delete Resource group and everything in it
    print('Delete Resource Group')
    delete_async_operation = resource_client.resource_groups.delete(GROUP_NAME)
    delete_async_operation.wait()
    print("Deleted: {}".format(GROUP_NAME))
    print("\n\n")


def print_item(group):
    """Print an Azure object instance."""
    print("\tName: {}".format(group.name))
    print("\tId: {}".format(group.id))
    print("\tLocation: {}".format(group.location))
    if hasattr(group, 'tags'):
        print("\tTags: {}".format(group.tags))
    if hasattr(group, 'properties'):
        print_properties(group.properties)


def print_metric(group):
    """Print an SQL metric."""
    print("\tResource Name: {}".format(group.resource_name))
    print("\tName: {}".format(group.display_name))
    print("\tValue: {}".format(group.current_value))
    print("\tUnit: {}".format(group.unit))


def print_properties(props):
    """Print a ResourceGroup properties instance."""
    if props and props.provisioning_state:
        print("\tProperties:")
        print("\t\tProvisioning State: {}".format(props.provisioning_state))
    print("\n\n")


if __name__ == "__main__":
    run_example()
