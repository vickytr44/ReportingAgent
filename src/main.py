# Fetch {number_of_records} {main_entity}  
# where {filter_conditions}  
# including {fields_to_fetch}  
# {optional_sorting_and_pagination} 

# Fetch {number_of_records} {main_entity}  
# where {filter_conditions}  
# including {fields_to_fetch_from_main_entity}  
# and {fields_to_fetch_from_related_entities} from {related_entities}  
# {optional_sorting_and_pagination}  

from model import model
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from graphql_client import execute_graphql_query
from prompt import escaped_system_prompt, error_resolver_prompt
from report_generator import create_pdf_report
from query_extractor import extract_graphql_query, query_extractor_lambda
from query_validator import validate_graphql_query
from schema_provider import get_escaped_schema, get_schema
from report_generator_v2 import generate_pdf_report
from entity_constants import *
# main_entity = "accounts"
# fields = "id, number, type"

# user_input_strict = f"""
# Fetch 3 {main_entity}  
# where customer name started with d or domestic account
# including {fields}
# sort based on account type in decending order.
# """

# main_entity = "customers"
# fields = "id, name, identityNumber, age"

# user_input_strict = f"""
# Fetch {main_entity}  
# where all accounts are active
# including {fields}
# """

main_entity = ACCOUNTS
fields_to_fetch_from_main_entity = "id, number, type"
fields_to_fetch_from_related_entities = "name, identityNumber, age"
related_entities = CUSTOMERS

user_input_strict = f"""
Fetch all {main_entity}  
where where customer name started with d or domestic account  
including {fields_to_fetch_from_main_entity}  
and {fields_to_fetch_from_related_entities} from {related_entities}   
"""

full_system_prompt = escaped_system_prompt + "\n### GraphQL Schema:\n" + get_escaped_schema(main_entity)

# Define prompt templates
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", full_system_prompt),
        ("human", "{userInput}"),
    ]
)

initial_chain = prompt_template | model | StrOutputParser() 

complete_chain = initial_chain | query_extractor_lambda

result_query = complete_chain.invoke({"userInput": user_input_strict})
print(result_query)

# Validate the query
validation_result = validate_graphql_query(result_query, get_schema(main_entity))

# Output validation results
print(validation_result)

final_query = result_query

escaped_result_query = result_query.replace("{", "{{").replace("}", "}}")

if validation_result:
    error_resolver_prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", error_resolver_prompt + "\n**GraphQL Query:**\n" + escaped_result_query + "\n**Validation Error:**\n" + validation_result + "\n### GraphQL Schema:\n" + get_escaped_schema(main_entity)),
            ("human", "{userInput}"),
        ]
    )

    error_resolver_chain = error_resolver_prompt_template | model | StrOutputParser()

    resolver_result = error_resolver_chain.invoke({"userInput": user_input_strict})
    print(resolver_result)
    final_query = extract_graphql_query(resolver_result)

print(final_query)

# json_data = execute_graphql_query(final_query)
# print(json_data)

# #create_pdf_report(main_entity, fields,json_data,"pdf_2")
# generate_pdf_report(final_query, json_data,"pdf_2")