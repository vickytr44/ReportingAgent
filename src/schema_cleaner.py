import re

def clean_graphql_schema(schema_text):
    # Remove all comments (single-line and multi-line)
    schema_text = re.sub(r'""".*?"""', '', schema_text, flags=re.DOTALL)  # Multi-line comments
    schema_text = re.sub(r'"[^"]*"', '', schema_text)  # Inline descriptions

    # Remove all @cost directives (regardless of the weight value)
    schema_text = re.sub(r'@cost\([^)]*\)', '', schema_text)

    # Remove @listSize directives
    schema_text = re.sub(r'@listSize\([^)]*\)', '', schema_text)

    # Remove directive @cost block completely
    schema_text = re.sub(
        r'directive\s+@cost\s*\([^)]*\)\s*on\s*[A-Z_| ]+\n?', '', schema_text
    )

    # Remove any remaining orphaned directive lines
    schema_text = re.sub(r'directive\s+[^\n]+\n?', '', schema_text)

    # Clean up extra spaces and empty lines
    schema_text = re.sub(r'\n\s*\n', '\n', schema_text).strip()

    return schema_text

# Example usage:
with open("schema.txt", "r") as file:
    original_schema = file.read()

cleaned_schema = clean_graphql_schema(original_schema)

with open("cleaned_schema.graphql", "w") as file:
    file.write(cleaned_schema)

print("Schema cleaned successfully!")

