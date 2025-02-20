from model import model
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from prompt import escaped_system_prompt, error_resolver_prompt
from query_extractor import extract_graphql_query, query_extractor_lambda
from query_validator import validate_graphql_query, get_escaped_validation_result
from schema_provider import get_escaped_schema, get_schema
from typing import Optional

def get_query_for_user_input(user_input_strict: str, main_entity: str) -> tuple[str, Optional[str]]:
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

    while process_retry_count < process_max_retries:
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
            print("Max retries reached. Could not resolve the query. Restating the process...")
            process_retry_count += 1

    return [final_query, validation_result]