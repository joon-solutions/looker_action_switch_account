import looker_sdk
import looker_sdk.sdk.api40.models as mdls
from typing import Optional
import logging

sdk = looker_sdk.init40("looker__stg.ini")

# def get_my_user():
#     """Fetch the currently authenticated user."""
#     my_user = sdk.me()
#     # first_name = my_user.first_name
#     # user_id = my_user.id
#     logging.info(f"Fetched user: {my_user.first_name} (ID: {my_user.id})")
#     return my_user.id  # Returning user_id to be used later

def get_user_id_by_email(email: str) -> Optional[str]:
    """Search for a user ID based on their email address."""
    try:
        logging.info(f"Searching for user with email: {email}")
        users = sdk.search_users(email=email, fields="id,email", limit=1)
        if not users:
            logging.warning(f"No user found with email: {email}")
            return None       
        user_id = users[0].id
        logging.info(f"User found: {email} -> User ID: {user_id}")
        return user_id
    except Exception as e:
        logging.error(f"Error searching for user by email: {e}")
        return None

def set_user_attribute_user_value(user_id: str, user_attribute_id: str, value: str):
    """Set a user attribute value for a specific user."""
    body = mdls.WriteUserAttributeWithValue(value=value)
    
    response = sdk.patch(
        f"/users/{user_id}/attribute_values/{user_attribute_id}",
        structure=mdls.UserAttributeWithValue,
        body=body
    )
    logging.info(f"Response: {response}")
    return response

def toggle_user_attr(user_id: str, attribute_id: str, attribute_value: str) -> str:
    allowed_values = ['external', 'internal']
    # allowed_values = ['ONE', 'Customer']
    current_value = attribute_value
    if current_value == allowed_values[0]:
        new_value = allowed_values[1] 
    elif current_value == allowed_values[1]:
        new_value = allowed_values[0] 
    else:
        new_value = 'external'


    # Create the UserAttributeWithValue object
    user_attr_value = mdls.WriteUserAttributeWithValue(
        value=new_value
    )

    # Update the user attribute value for the specified user
    response = sdk.set_user_attribute_user_value(user_id=user_id, 
                                      user_attribute_id=attribute_id, 
                                      body=user_attr_value)
    return str(response)