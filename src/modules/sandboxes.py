"""
Sandbox API client library
"""
import requests
import modules.endpoints as endpoints
import modules.logger as logger
import modules.xml_parser as xml_parser
from requests.auth import HTTPBasicAuth

class Sandboxes(object):
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.logger = logger.Logger()
        self.xml_parser = xml_parser.XmlParser()
        return

    def get_sandboxes(self, app_id):
        sandboxes = []
        try:
            response = self.xml_parser.parse_xml(requests.post(endpoints.GET_SANDBOXES, auth=HTTPBasicAuth(self.user, self.password), data={'app_id': app_id}).text)
            for sandbox in response:
                if self.sandbox_response_is_valid(sandbox) and sandbox not in sandboxes:
                    sandboxes.append({
                        'sandbox_id': sandbox.attrib['sandbox_id'],
                        'builds': []
                    })
        except Exception as e:
            self.logger.exception('Exception getting sandboxes for applidation: {}, {}'.format(app_id, e))
        return sandboxes
    
    def sandbox_response_is_valid(self, sandbox):
        return sandbox is not None and sandbox.attrib is not None and sandbox.attrib['sandbox_id'] is not None