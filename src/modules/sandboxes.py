"""
Sandbox API client library
"""
import requests
import modules.endpoints as endpoints
import modules.logger as logger
import modules.constants as constants
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
            self.logger.info('Attempting to retrieve sandboxes for app: {}'.format(app_id))
            resp = requests.post(endpoints.GET_SANDBOXES, auth=HTTPBasicAuth(self.user, self.password), data={'app_id': app_id}, timeout=constants.REQUEST_TIMEOUT)
            if resp.status_code == 200:
                # self.logger.info('Response to get sandbox: {}'.format(resp.text))
                response = self.xml_parser.parse_xml(resp.text)
                for sandbox in response:
                    self.logger.info('Testing validity of sandbox: {}'.format(sandbox))
                    if self.sandbox_response_is_valid(sandbox) and sandbox not in sandboxes:
                        sandboxes.append({
                            'sandbox_id': sandbox.attrib['sandbox_id'],
                            'builds': []
                        })
            else:
                raise Exception('Authentication error: {}'.format(resp.status_code))
        except Exception as e:
            self.logger.exception('Exception getting sandboxes for application: {}, {}'.format(app_id, e))
        return sandboxes

    def sandbox_response_is_valid(self, sandbox):
        self.logger.info('Inside sandbox validity check')
        return sandbox is not None and sandbox.attrib is not None and sandbox.attrib['sandbox_id'] is not None
