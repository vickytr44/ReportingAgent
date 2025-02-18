from langchain.schema.runnable import RunnableLambda
import re

# def extract_graphql_query(text):
#     match = re.search(r"```graphql\s*(.*?)\s*```", text, re.DOTALL)
#     return match.group(1) if match else None


def extract_graphql_query(response: str) -> str:
    match = re.search(r"```(?:graphql)?\n(.*?)\n```", response, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Fallback: Detect query without code block
    match = re.search(r"(query\s*\{.*?\})", response, re.DOTALL)
    return match.group(1).strip() if match else ""

query_extractor_lambda = RunnableLambda(lambda x: extract_graphql_query(x))