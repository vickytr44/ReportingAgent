from account_schema_graphql import escaped_account_schema_graphql, account_schema_graphql
from customer_schema_graphql import escaped_customer_schema_graphql, customer_schema_graphql
from bill_schema_graphql import escaped_bill_schema_graphql, bill_schema_graphql
from entity_constants import *

def get_escaped_schema(main_entity):
    schema_mapping = {
        ACCOUNTS: escaped_account_schema_graphql,
        CUSTOMERS: escaped_customer_schema_graphql,
        BILLS: escaped_bill_schema_graphql
    }
    try:
        return schema_mapping[main_entity]
    except KeyError:
        raise ValueError("Unknown main entity")

def get_schema(main_entity):
    schema_mapping = {
        ACCOUNTS: account_schema_graphql,
        CUSTOMERS: customer_schema_graphql,
        BILLS: bill_schema_graphql
    }
    try:
        return schema_mapping[main_entity]
    except KeyError:
        raise ValueError("Unknown main entity")