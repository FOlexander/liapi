from linkedin_api import Linkedin
import json

def get_profile_data(profile_id):
    # Authenticate using any Linkedin user account credentials
    api = Linkedin('prodigy86@ex.ua', 'Karandash17')

    profile_id = profile_id.split("/")[-2]
    profile_data = api.get_profile(profile_id)
    profile_string = json.dumps(profile_data)
    return profile_string

if __name__ == '__main__':
    get_profile_data('bikiviki')