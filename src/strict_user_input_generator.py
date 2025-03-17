# Fetch {number_of_records} {main_entity}  
# where {filter_conditions}  
# including {fields_to_fetch}  
# {optional_sorting_and_pagination} 

# Fetch {number_of_records} {main_entity}  
# where {filter_conditions}  
# including {fields_to_fetch_from_main_entity}  
# and {fields_to_fetch_from_related_entities} from {related_entities}  
# {optional_sorting_and_pagination}  

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

# user_input_strict = f"""
# Fetch all {main_entity}  
# where customer name started with d or domestic account and bill amount is greater than 1000 
# including {fields_to_fetch_from_main_entity}  
# and {fields_to_fetch_from_related_entities1} from {related_entities1}   
# and {fields_to_fetch_from_related_entities2} from {related_entities2}
# sort based on customer name in decending order.
# """

# user_input_strict = f"""
# Fetch all {main_entity} where:
# - Any of the following must be true:  
#   - {or_condition_1}  
#   - {or_condition_2}  
  
# - And all of the following must be true:  
#   - {and_condition_1}  

# Include the following fields:  
# - **{main_entity}**: {fields_to_fetch_from_main_entity}  
# - **{related_entity_1}**: {fields_to_fetch_from_related_entity_1}  
# - **{related_entity_2}**: {fields_to_fetch_from_related_entity_2}  

# Sort results by:
# - **{sort_field_1}** in **{sort_order_1}** order   
# """

def generate_strict_user_input(main_entity : str, fields_to_fetch_from_main_entity : str , or_conditions : list, and_conditions : list, related_entity_fields : dict, sort_field_order : dict) -> str:
    
    or_condition_line = ""
    and_condition_line = ""
    sort_line = ""

    first_line = f"""
    Fetch all {main_entity} where:"""

    if(or_conditions):
        or_condition_line = f"""
        - Any of the following must be true:"""

        for condition in or_conditions:
            or_condition_line += f"""
        - {condition}""" 
        
    if(and_conditions):
        and_condition_line = f"""
        - And all of the following must be true:"""
        for condition in and_conditions:
            and_condition_line += f"""
        - {condition}"""

    include_fields_line = f"""
    Include the following fields:
    - **{main_entity}**: {fields_to_fetch_from_main_entity}"""

    if(related_entity_fields):
        for related_entity, fields in related_entity_fields.items():
            include_fields_line += f"""
        - **{related_entity}**: {fields}"""

    if(sort_field_order):
        sort_line = f"""
        Sort results by:"""

        for field, order in sort_field_order.items():
            sort_line += f"""
        - **{field}** in **{order}** order"""
        
    user_input_strict = first_line + "\n" + or_condition_line + "\n" + and_condition_line + "\n" + include_fields_line + "\n" + sort_line

    return user_input_strict
