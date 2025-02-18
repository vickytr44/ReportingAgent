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
from query_validator import validate_graphql_query, get_escaped_validation_result
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

# main_entity = ACCOUNTS
# fields_to_fetch_from_main_entity = "id, number, type"
# fields_to_fetch_from_related_entities = "name, identityNumber, age"
# related_entities = CUSTOMERS

# user_input_strict = f"""
# Fetch all {main_entity}  
# where customer name started with d or domestic account  
# including {fields_to_fetch_from_main_entity}  
# and {fields_to_fetch_from_related_entities} from {related_entities}   
# """

main_entity = BILLS
fields_to_fetch_from_main_entity = "number, month, dueDate, amount"
fields_to_fetch_from_related_entity_1 = "name, identityNumber, age"
related_entity_1 = CUSTOMERS
fields_to_fetch_from_related_entity_2 = "id, number, type"
related_entity_2 = ACCOUNTS
or_condition_1 = "customer name starts with d"
or_condition_2 = "account type is domestic "
and_condition_1 = "bill amount is greater than 1000"
sort_field_1 = "customer name"
sort_order_1 = "decending"
# user_input_strict = f"""
# Fetch all {main_entity}  
# where customer name started with d or domestic account and bill amount is greater than 1000 
# including {fields_to_fetch_from_main_entity}  
# and {fields_to_fetch_from_related_entities1} from {related_entities1}   
# and {fields_to_fetch_from_related_entities2} from {related_entities2}
# sort based on customer name in decending order.
# """

user_input_strict = f"""
Fetch all {main_entity} where:
- Any of the following must be true:  
  - {or_condition_1}  
  - {or_condition_2}  
  
- And all of the following must be true:  
  - {and_condition_1}  

Include the following fields:  
- **{main_entity}**: {fields_to_fetch_from_main_entity}  
- **{related_entity_1}**: {fields_to_fetch_from_related_entity_1}  
- **{related_entity_2}**: {fields_to_fetch_from_related_entity_2}  

Sort results by:
- **{sort_field_1}** in **{sort_order_1}** order   
"""

print(user_input_strict)

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

process_retry_count = 0
process_max_retries = 3

while True and process_retry_count < process_max_retries:
    print("Resolving the query...")
    result_query = complete_chain.invoke({"userInput": user_input_strict})

    # Validate the query
    validation_result = validate_graphql_query(result_query, get_schema(main_entity))

    final_query = result_query

    escaped_result_query = result_query.replace("{", "{{").replace("}", "}}")

    retry_count = 0
    max_retries = 3

    while validation_result and retry_count < max_retries:
        print(f"validation retry: {retry_count}")
        error_resolver_prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", error_resolver_prompt + "\n**GraphQL Query:**\n" + escaped_result_query + "\n**Validation Error:**\n" + get_escaped_validation_result(validation_result) + "\n### GraphQL Schema:\n" + get_escaped_schema(main_entity)),
                ("human", "{userInput}"),
            ]
        )

        error_resolver_chain = error_resolver_prompt_template | model | StrOutputParser()

        resolver_result = error_resolver_chain.invoke({"userInput": user_input_strict})
        final_query = extract_graphql_query(resolver_result)
        validation_result = validate_graphql_query(final_query, get_schema(main_entity))
        retry_count += 1

    if not validation_result:
        break

    if validation_result and retry_count == max_retries:
        print("Max retries reached. Could not resolve the query.Restating the process...")
        process_retry_count += 1

print(final_query)

json_data = execute_graphql_query(final_query)
print(json_data)

#create_pdf_report(main_entity, fields,json_data,"pdf_2")
generate_pdf_report(final_query, json_data,"pdf_2")