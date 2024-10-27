import os
import json
from dotenv import load_dotenv
from linkedin_api import Linkedin

load_dotenv()  
mail = os.getenv("MAIL_F")
password = os.getenv("PASSWORD_F")

def get_profile_data(profile_id):
    # Authenticate using any Linkedin user account credentials
    api = Linkedin(mail, password)

    profile_id = profile_id.split("/")[-2]
    profile_data = api.get_profile(profile_id)
    profile_string = json.dumps(profile_data)
    return profile_string

if __name__ == '__main__':
    get_profile_data('bikiviki')