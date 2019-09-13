---
page_type: sample
languages:
- python
products:
- azure
description: "This sample shows how to manage SQL Server using the Azure Storage Resource Provider for Python."
urlFragment: sql-database-python-manage
---

# Getting Started with Azure SQL Management in Python

This sample shows how to manage SQL Server using the Azure Storage Resource Provider for Python.

**On this page**

- [Run this sample](#run)
- [What is example.py doing?](#example)
    - [Create a SQL Server instance](#create-server)
    - [Create a Firewall rule](#create-firewall-rule)
    - [List servers by resource group](#list-servers-by-resource-group)
    - [List servers by subscription](#list-servers-by-subscription)
    - [List server usages](#list-server-usages)
    - [Create a database](#create-database)
    - [Get a database](#get-database)
    - [List databases](#list-databases)
    - [List database usages](#list-database-usages)
    - [Delete a database](#delete-database)
    - [Delete a SQL Server instance](#delete-server)
- [More information](#more-info)

<a name="run"></a>
## Run this sample

1. If you don't already have it, [install Python](https://www.python.org/downloads/).

2. We recommend using a [virtual environment](https://docs.python.org/3/tutorial/venv.html) to run this example, but it's not mandatory. You can initialize a virtual environment this way:

    ```
    pip install virtualenv
    virtualenv mytestenv
    cd mytestenv
    source bin/activate
    ```

3. Clone the repository.

    ```
    git clone https://github.com/Azure-Samples/sql-database-python-manage.git
    ```

4. Install the dependencies using pip.

    ```
    cd sql-database-python-manage
    pip install -r requirements.txt
    ```

5. Create an Azure service principal, using 
[Azure CLI](http://azure.microsoft.com/documentation/articles/resource-group-authenticate-service-principal-cli/),
[PowerShell](http://azure.microsoft.com/documentation/articles/resource-group-authenticate-service-principal/)
or [Azure Portal](http://azure.microsoft.com/documentation/articles/resource-group-create-service-principal-portal/).

6. Export these environment variables into your current shell. 

    ```
    export AZURE_TENANT_ID={your tenant id}
    export AZURE_CLIENT_ID={your client id}
    export AZURE_CLIENT_SECRET={your client secret}
    export AZURE_SUBSCRIPTION_ID={your subscription id}
    ```

7. Run the sample.

    ```
    python example.py
    ```

<a id="example"></a>
## What is example.py doing?

The sample walks you through several SQL Server operations.
It starts by setting up a ResourceManagementClient and SQLManagementClient objects
using your subscription and credentials.

```python
#
# Create the Resource Manager Client with an Application (service principal) token provider
#
subscription_id = os.environ.get(
    'AZURE_SUBSCRIPTION_ID',
    '11111111-1111-1111-1111-111111111111') # your Azure Subscription Id
credentials = ServicePrincipalCredentials(
    client_id=os.environ['AZURE_CLIENT_ID'],
    secret=os.environ['AZURE_CLIENT_SECRET'],
    tenant=os.environ['AZURE_TENANT_ID']
)
resource_client = ResourceManagementClient(credentials, subscription_id)
sql_client = SqlManagementClient(credentials, subscription_id)

# You MIGHT need to add SQL as a valid provider for these credentials
# If so, this operation has to be done only once for each credential
resource_client.providers.register('Microsoft.Sql')

# Create Resource group
resource_group_params = {'location':'westus'}
resource_client.resource_groups.create_or_update(GROUP_NAME, resource_group_params)
```

There are also a few supporting functions (`print_item`, `print_metrics`, and `print_properties`).

<a id="create-server"></a>
### Create a SQL Server instance

```python
server = sql_client.servers.create_or_update(
    GROUP_NAME,
    SERVER_NAME,
    {
        'location': REGION,
        'version': '12.0', # Required for create
        'administrator_login': 'mysecretname', # Required for create
        'administrator_login_password': 'HusH_Sec4et' # Required for create
    }
)
```

<a id="create-firewall-rule"></a>
### Create a firewall rule

```python
firewall_rule = sql_client.servers.create_or_update_firewall_rule(
    GROUP_NAME,
    SERVER_NAME,
    "firewall_rule_name_123.123.123.123",
    "123.123.123.123", # Start ip range
    "123.123.123.123"  # End ip range
)
```

<a id="get-server"></a>
### Get a server

```python
server = sql_client.servers.get_by_resource_group(
    GROUP_NAME,
    SERVER_NAME,
)
```


<a id="list-servers-by-resource-group"></a>
### List servers by resource group

```python
sql_client.servers.list_by_resource_group(GROUP_NAME)
```

<a id="list-servers-by-subscription"></a>
### List servers by subscription

```python
sql_client.servers.list()
```

<a id="list-server-usages"></a>
### List server usages

```python
sql_client.servers.list_usages(GROUP_NAME, SERVER_NAME)
```

<a id="create-database"></a>
### Create a database

```python
async_db_create = sql_client.databases.create_or_update(
    GROUP_NAME,
    SERVER_NAME,
    DATABASE_NAME,
    {
        'location': REGION
    }
)
database = async_db_create.result() # Wait for completion and return created object
```

<a id="get-database"></a>
### Get a database

```python
database = sql_client.databases.get(
    GROUP_NAME,
    SERVER_NAME,
    DATABASE_NAME
)
```

<a id="list-databases"></a>
### Get a list of databases

```python
sql_client.databases.list_by_server(GROUP_NAME, SERVER_NAME)
```

<a id="list-usages"></a>
### Get a list of database usages

```python
sql_client.databases.list_usages(GROUP_NAME, SERVER_NAME, DATABASE_NAME)
```

<a id="delete-database"></a>
### Delete a database

```python
sql_client.databases.delete(GROUP_NAME, SERVER_NAME, DATABASE_NAME)
```

<a id="delete-server"></a>
### Delete a SQL Server instance

```python
sql_client.servers.delete(GROUP_NAME, SERVER_NAME)
```

<a name="more-info"></a>
## More information

- [Azure SDK for Python](http://github.com/Azure/azure-sdk-for-python) 
- [Azure SQL Documentation](https://azure.microsoft.com/services/sql-database/)
