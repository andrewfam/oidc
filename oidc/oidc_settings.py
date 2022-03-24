import json

from django.core.serializers import serialize

from oidc_provider.lib.claims import ScopeClaims

def userinfo(claims, user):
    claims['email'] = user.email

    json_str_response = serialize('json', [user.profile], ensure_ascii=False)
    response = json.loads(json_str_response)

    claims['profile'] = response
    claims['given_name'] = user.profile.first_name
    claims['family_name'] = user.profile.last_name
    
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