import os
import json
from dotenv import load_dotenv
from linkedin_api import Linkedin
import cookies


load_dotenv()  
mail = os.getenv("MAIL_F")
password = os.getenv("PASSWORD_F")

def get_profile_data(profile_id):

    cook = cookies.make_cookie()
    # Authenticate using any Linkedin user account credentials
    api = Linkedin(mail, password, cookies=cook)

    profile_id = profile_id.split("/")[-2]
    profile_data = api.get_profile(profile_id)

    # Save the dictionary as a JSON file
    # with open("profile_data.json", "w") as json_file:
    #     json.dump(profile_data, json_file, indent=4)  

    profile_urn = profile_data['urn_id']
    exp_data = api.get_profile_experiences(profile_urn)
    
    exp_string = json.dumps(exp_data)
    profile_string = json.dumps(profile_data)
    print(exp_string)
    return (profile_string, exp_string)

if __name__ == '__main__':
    ps, es = get_profile_data('afurmanenko')
    print(ps)