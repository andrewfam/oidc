import json

from django.core.serializers import serialize

from oidc_provider.lib.claims import ScopeClaims

def userinfo(claims, user):
    # Populate claims dict.
    claims['name'] = '{0} {1}'.format(user.first_name, user.last_name)
    claims['given_name'] = user.first_name
    claims['family_name'] = user.last_name
    claims['email'] = user.email
    claims['address']['street_address'] = '...'

    return claims

class CustomScopeClaims(ScopeClaims):
    info_details = (
            ('User Meta Data'),
            ('List of details such as ID Number, Last Logout, and Access Rights'),
        )

    def scope_details(self):
        json_str_response = serialize('json', [self.user.profile])
        response = json.loads(json_str_response)
        
        responses = {
            'user_profile': response,
            'id_number': self.user.id_number,
            'last_login' : self.user.last_login,
            'last_logout' : self.user.last_logout,
            'user_type' : self.user.user_type,
        }

        return responses