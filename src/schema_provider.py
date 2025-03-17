from entity_constants import *
from graphql_client import execute_graphql_query

def get_escaped_schema(main_entity):
    try:
        schema = get_schema(main_entity).replace("{", "{{").replace("}", "}}")
        return schema
    except KeyError:
        raise ValueError("Unknown main entity")

def get_schema(main_entity):
    query: str = "{" + f"""cleanedSchema(schemaName: "{main_entity}")""" + "}"
    try:
        result = execute_graphql_query(query).get("cleanedSchema")
        return result
    except KeyError:
        raise ValueError("Unknown main entity")
    