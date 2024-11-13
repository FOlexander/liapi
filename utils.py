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

    # profile_id = profile_id.split("/")[-2]
    profile_data = api.get_profile(profile_id)
    exp_data = api.get_profile_experiences(profile_id)
    with open('prof_data.json', 'w') as outfile:
        json.dump(profile_data, outfile)
    with open('exp_data.json', 'w') as outfile:
        json.dump(exp_data, outfile)
    # profile_string = json.dumps(profile_data)
    # return profile_string

if __name__ == '__main__':
    get_profile_data('ACoAAATAn-sBUQKSxd4ZbAroWQ1CQ2mZC3j4wbM')