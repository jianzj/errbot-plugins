import requests
from requests import HTTPError
import json

from errbot import BotPlugin


class PagerDuty(BotPlugin):
    
    def activate(self):
        super().activate()
        
        # Initialization
        self.utils = self.get_plugin("UtilsFunc")
        self.extraConfig = self.get_plugin("ExtraConfig")
        self.pdConfig = self.extraConfig.load("PagerDuty")
        self.pdc = HTTPClient(self.pdConfig['url'], self.pdConfig['token'])

    def get_service(self, serviceId):
        
        if not serviceId:
            self.log.error("No ServiceID provided !")
            return None
        
        url = "/services/%s" % serviceId
        service = self.pdc.get(url)
        return service

    def get_user(self, userId):
        
        if not userId:
            self.log.error("No UserID provided !")
            return None

        url = "/users/%s" % userId
        user = self.pdc.get(url)
        return user

    def find_user_byEmail(self, email):

        if not email:
            self.log.error("No Email provided !")
        url = "/users"
        params = {"query": email}

        resp = self.pdc.get(url, params=params)
        users = resp['users']

        if len(users) > 0 : return users[0]
        return None


class HTTPClient(object):

    def __init__(self, base_url, api_token):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({'Authorization': 'Token token=' + api_token})
        self.session.headers.update({"Content-Type": "application/json"})

    def _request(self, url, method, headers=None, params=None, data=None, **kwargs):
        request_path = "%s%s" % (self.base_url, url)
        try:
            response = self.session.request(method=method,
                                            url=request_path,
                                            headers=headers,
                                            params=params,
                                            data=data,
                                            **kwargs) 
            self._handle_response(response)
    
            if not response.text:
                return None
            return json.loads(response.text)
        except Exception as e:
            return None

    def get(self, url, headers=None, params=None, **kwargs):
        return self._request(url=url, method="GET",
                             headers=headers, params=params, **kwargs)

    def post(self, url, headers=None, params=None, data=None, **kwargs):
        return self._request(url=url, method="POST",
                             headers=headers, params=params, data=data, **kwargs)

    def put(self, url, headers=None, params=None, data=None, **kwargs):
        return self._request(url=url, method="PUT",
                             headers=headers, params=params, data=data, **kwargs)

    def delete(self, url, headers=None, params=None, **kwargs):
        return self._request(url=url, method="DELETE",
                             headers=headers, params=params, **kwargs)

    def _handle_response(self, response):
        if not response:
            raise HTTPError("No response found, unexpected errors happened.")

        if not self.is_expected_status_code(response.request.method,
                                            response.status_code):
            raise HTTPError("Issue occur during HTTP request, METHOD:"
                            " %s, URL: %s, Return code: %s, "
                            "Response text: %s" % (response.request.method,
                                                   response.request.url,
                                                   response.status_code,
                                                   response.text))

    def is_expected_status_code(self, method, response_code):
        mapping = {"GET": [200], 
                   "POST": [201],
                   "DELETE": [204, 202],
                   "PUT": [202]}
        if mapping[method] and response_code in mapping[method]:
            return True
        return False