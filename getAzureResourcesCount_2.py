import os
from azure.common.credentials import ServicePrincipalCredentials
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient


# TODO use either this or below one
# def __get_authentication():
#     subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", "SOME_AZURE_SUBSCRIPTION_ID")
#     credentials = ClientSecretCredential(
#         client_id=os.environ.get("AZURE_CLIENT_ID", "SOME_AZURE_CLIENT_ID"),
#         secret=os.environ.get("AZURE_CLIENT_SECRET", "SOME_AZURE_CLIENT_SECRET"),
#         tenant=os.environ.get("AZURE_TENANT_ID", "SOME_AZURE_TENANT_ID")
#     )
#     return credentials, subscription_id


def __get_authentication():
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", "SOME_AZURE_SUBSCRIPTION_ID")
    credentials = ServicePrincipalCredentials(
        client_id=os.environ.get("AZURE_CLIENT_ID", "SOME_AZURE_CLIENT_ID"),
        secret=os.environ.get("AZURE_CLIENT_SECRET", "SOME_AZURE_CLIENT_SECRET"),
        tenant=os.environ.get("AZURE_TENANT_ID", "SOME_AZURE_TENANT_ID")
    )
    return credentials, subscription_id


def __getTotalCountForAzureResourceGroups():
    credentials, subscription_id = __get_authentication()
    client = ResourceManagementClient(credentials, subscription_id)
    total = 0
    for rg in client.resource_groups.list():
        total = total + 1
    return total


def __getTotalCountForAzureSqlServers():
    credentials, subscription_id = __get_authentication()
    client = SqlManagementClient(credentials, subscription_id)
    total = 0
    for item in client.servers.list():
        total = total + 1
    return total


def __getTotalCountForAzureSqlServerDatabase():
    credentials, subscription_id = __get_authentication()
    client = SqlManagementClient(credentials, subscription_id)
    total = 0
    for server in client.servers.list():
        group = server.id.split('/')
        for db in client.databases.list_by_server(group[4], server.name):
            if db.name != 'master':
                total = total + 1
    return total


def __getTotalCountForAzureWebApps():
    credentials, subscription_id = __get_authentication()
    client = WebSiteManagementClient(credentials, subscription_id)
    total = 0
    for site in client.web_apps.list():
        if 'functionapp' not in site.kind:
            total = total + 1
    return total


def __getTotalCountForAzureFunctionApps():
    credentials, subscription_id = __get_authentication()
    client = WebSiteManagementClient(credentials, subscription_id)
    total = 0
    for site in client.web_apps.list():
        if 'functionapp' in site.kind:
            total = total + 1
    return total


def __getTotalCountForAzureVirtualMachines():
    credentials, subscription_id = __get_authentication()
    client = ComputeManagementClient(credentials, subscription_id)
    total = 0
    for vm in client.virtual_machines.list_all():
        total = total + 1
    return total


def __getTotalCountForAzureVirtualNetwork():
    credentials, subscription_id = __get_authentication()
    client = NetworkManagementClient(credentials, subscription_id)
    total = 0
    for vn in client.virtual_networks.list_all():
        total = total + 1
    return total


def __getTotalCountForAzureNetworkSecurityGroup():
    credentials, subscription_id = __get_authentication()
    client = NetworkManagementClient(credentials, subscription_id)
    total = 0
    for nsg in client.network_security_groups.list_all():
        total = total + 1
    return total


def getAzureTotalCountByLocation(resourceName, locationName):
    total = 0
    credentials, subscription_id = __get_authentication()
    if resourceName == 'Resource Group':
        client = ResourceManagementClient(credentials, subscription_id)
        for rg in client.resource_groups.list():
            location = rg.location
            if locationName == location:
                total = total + 1
    elif resourceName == 'SQL Server':
        client = SqlManagementClient(credentials, subscription_id)
        for item in client.servers.list():
            location = item.location
            if locationName == location:
                total = total + 1
    elif resourceName == 'Function App':
        client = WebSiteManagementClient(credentials, subscription_id)
        for site in client.web_apps.list():
            location = site.location
            if locationName == location:
                if 'functionapp' in site.kind:
                    total = total + 1
    elif resourceName == 'Virtual Network':
        client = NetworkManagementClient(credentials, subscription_id)
        for vn in client.virtual_networks.list_all():
            location = vn.location
            if locationName == location:
                total = total + 1
    elif resourceName == 'Virtual Machine':
        client = ComputeManagementClient(credentials, subscription_id)
        for vm in client.virtual_machines.list_all():
            location = vm.location
            if locationName == location:
                total = total + 1
    elif resourceName == 'Network Security Group':
        client = NetworkManagementClient(credentials, subscription_id)
        for nsg in client.network_security_groups.list_all():
            location = nsg.location
            if locationName == location:
                total = total + 1
    elif resourceName == 'Web App':
        client = WebSiteManagementClient(credentials, subscription_id)
        for site in client.web_apps.list():
            location = site.location
            if locationName == location:
                if 'functionapp' not in site.kind:
                    total = total + 1
    elif resourceName == 'SQL Server Database':
        client = SqlManagementClient(credentials, subscription_id)
        for server in client.servers.list():
            location = server.location
            if locationName == location:
                group = server.id.split('/')
                for db in client.databases.list_by_server(group[4], server.name):
                    if db.name != 'master':
                        total = total + 1
    else:
        total = 0
    print(total)
    return total


def getAzureTotalCountOfResource(resourceName):
    if resourceName == 'SQL Server':
        total = __getTotalCountForAzureSqlServers()
    elif resourceName == 'Function App':
        total = __getTotalCountForAzureFunctionApps()
    elif resourceName == 'SQL Server Database':
        total = __getTotalCountForAzureSqlServerDatabase()
    elif resourceName == 'Resource Group':
        total = __getTotalCountForAzureResourceGroups()
    elif resourceName == 'Virtual Network':
        total = __getTotalCountForAzureVirtualNetwork()
    elif resourceName == 'Virtual Machine':
        total = __getTotalCountForAzureVirtualMachines()
    elif resourceName == 'Network Security Group':
        total = __getTotalCountForAzureNetworkSecurityGroup()
    elif resourceName == 'Web App':
        total = __getTotalCountForAzureWebApps()
    else:
        total = 0
    return total
