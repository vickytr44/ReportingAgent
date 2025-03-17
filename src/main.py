from entity_constants import *
from report_generator_v2 import generate_pdf_report
from strict_user_input_generator import generate_strict_user_input
from query_generator import get_query_for_user_input
from graphql_client import execute_graphql_query
from fastapi import HTTPException, FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# main_entity = BILLS
# fields_to_fetch_from_main_entity = "number, month, dueDate, amount"
# fields_to_fetch_from_related_entity_1 = "name, identityNumber, age"
# related_entity_1 = CUSTOMERS
# fields_to_fetch_from_related_entity_2 = "id, number, type"
# related_entity_2 = ACCOUNTS
# or_condition_1 = "customer name starts with d"
# or_condition_2 = "account type is domestic "
# and_condition_1 = "bill amount is greater than 1000"
# sort_field_1 = "customer name"
# sort_order_1 = "decending"


# or_conditions = []
# and_conditions = []
# related_entity_fields = {}
# sort_field_order = {}

# or_conditions.append(or_condition_1)
# or_conditions.append(or_condition_2)
# and_conditions.append(and_condition_1)
# related_entity_fields[related_entity_1] = fields_to_fetch_from_related_entity_1
# related_entity_fields[related_entity_2] = fields_to_fetch_from_related_entity_2
# sort_field_order[sort_field_1] = sort_order_1

class ReportRequest(BaseModel):
    main_entity: str
    fields_to_fetch_from_main_entity: Optional[str] = None
    or_conditions: Optional[List[str]] = None
    and_conditions: Optional[List[str]] = None
    related_entity_fields: Optional[Dict[str, str]] = None
    sort_field_order: Optional[Dict[str, str]] = None


@app.post("/generate-report")
def generate_query(request: ReportRequest):

    user_input_strict = generate_strict_user_input(
        request.main_entity, request.fields_to_fetch_from_main_entity, request.or_conditions, request.and_conditions, request.related_entity_fields, request.sort_field_order
    )

    query, validation = get_query_for_user_input(user_input_strict, request.main_entity)

    if validation:
        raise HTTPException(status_code=400, detail="Could not resolve the query. Please try again.")

    print(query)
    
    json_data = execute_graphql_query(query)
    print(json_data)

    #create_pdf_report(main_entity, fields,json_data,"pdf_2")
    pdf_stream = generate_pdf_report(query, json_data)
    return StreamingResponse(pdf_stream, media_type="application/pdf", headers={"Content-Disposition": "attachment"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
