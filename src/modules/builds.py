"""
"""
import requests
from datetime import date
import modules.endpoints as endpoints
import modules.logger as logger
import modules.constants as constants
import modules.xml_parser as xml_parser
from requests.auth import HTTPBasicAuth
import modules.constants as constants
from modules.month_to_integer_conversion import MonthToIntegerConverter

class Builds(object):
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.logger = logger.Logger()
        self.xml_parser = xml_parser.XmlParser()
        self.month_to_integer_conversion = MonthToIntegerConverter()
        return

    def get_builds(self, app_id, sandbox_id):
        builds = []
        try:
            self.logger.info('Attempting to retrieve builds for app: {} and sandbox: {}'.format(app_id, sandbox_id))
            resp = requests.post(endpoints.GET_SANDBOX_BUILD_LIST, auth=HTTPBasicAuth(self.user, self.password), data={'app_id': app_id, 'sandbox_id': sandbox_id}, timeout=constants.REQUEST_TIMEOUT)
            if resp.status_code == 200:
                response = self.xml_parser.parse_xml(resp.text)
                self.logger.info('Received response for request: {}'.format(resp))
                for build in response:
                    if self.get_builds_response_is_valid(build) and build not in builds:
                        builds.append({
                            'build_id': build.attrib['build_id'],
                            'date': build.attrib['version'],
                            'submitter': ''
                        })
            else:
                raise Exception('Authentication error: {}'.format(resp.status_code))
        except Exception as e:
            self.logger.exception('Exception getting sandbox builds for application: {} and sandbox: {}, {}'.format(app_id, sandbox_id, e))
        return builds

    def get_builds_response_is_valid(self, build):
        return self.get_days_since_build(build) < constants.BUILD_MAX_AGE_FOR_VALIDITY and build is not None and build.attrib is not None and build.attrib['build_id'] is not None

    def get_days_since_build(self, build):
        build_date_data = build.attrib['version'][0:build.attrib['version'].find('Static')].split(' ')
        build_date = date(int(build_date_data[2]), self.month_to_integer_conversion.get_month(build_date_data[1]), int(build_date_data[0]))
        today = date.today()
        return abs(today - build_date).days

    def get_build_response_is_valid(self, build):
        return build is not None and build.attrib is not None and build.attrib['submitter'] is not None

    def get_build(self, app_id, build_id):
        submitter = ''
        try:
            self.logger.info('Attempting to retrieve build: {}, for app: {}'.format(build_id, app_id))
            resp = requests.post(endpoints.GET_BUILD_INFO, auth=HTTPBasicAuth(self.user, self.password), data={'app_id': app_id, 'build_id': build_id}, timeout=constants.REQUEST_TIMEOUT)
            if resp.status_code == 200:
                response = self.xml_parser.parse_xml(resp.text)
                for build in response:
                    if self.get_build_response_is_valid(build):
                        submitter = build.attrib['submitter']
            else:
                raise Exception('Authentication error: {}'.format(resp.status_code))
        except Exception as e:
            self.logger.error('Exception retrieving build details for app: {}, build: {}, {}'.format(app_id, build_id, e))
        return submitter
