"""
Application API client
"""
import requests
import sys
import modules.endpoints as endpoints
import modules.xml_parser as xml_parser
import modules.constants as constants
from modules.logger import Logger
from requests.auth import HTTPBasicAuth

class Applications(object):
    def __init__(self, user, password):
        self.logger = Logger()
        self.xml_parser = xml_parser.XmlParser()
        self.user = user
        self.password = password
        return

    def get_apps(self):
        apps = []
        try:
            self.logger.info('Attempting to get applications!!!')
            resp = requests.post(endpoints.REQUEST_APPS, auth=HTTPBasicAuth(self.user, self.password))
            if resp.status_code == 200:
                response = self.xml_parser.parse_xml(resp.text)
                for item in response:
                    if item.attrib['app_id'] is not None and not item.attrib['app_id'] in apps:
                        apps.append({
                            'app_id': item.attrib['app_id'],
                            'app_name': item.attrib['app_name'],
                            'sandboxes': []
                        })
                self.logger.info('Successfully retrieved app list!')
            else:
                self.logger.error('Authentication Issue: {}'.format(resp.status_code))
        except Exception as e:
            self.logger.exception('Error retrieving app list: {}'.format(e))
        return apps

