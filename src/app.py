"""
Main runtime for Veracode sandbox scan reporting
"""

import os
import sys

from modules.logger import Logger
from modules.sandboxes import Sandboxes
from modules.builds import Builds
from modules.applications import Applications
from modules.mailer import Mailer
from modules.spreadsheet_creator import SpreadsheetCreator
import modules.constants as constants

class App(object):
    def __init__(self):
        self.logger = Logger()
        user = os.getenv('VC_USER')
        password = os.getenv('VC_PASS')
        
        if not self.should_run(user, password):
            self.logger.error('User or password is not defined, exiting...')
            sys.exit()
        
        self.sandboxes = Sandboxes(user, password)
        self.applications = Applications(user, password)
        self.builds = Builds(user, password)
        self.spreadsheet_creator = SpreadsheetCreator()
        apps = self.applications.get_apps()
        self.get_app_sandboxes(apps)
        self.get_app_sandbox_builds(apps)
        self.get_builds(apps)
        self.create_spreadsheet(apps)
        self.send_message()
    
    def should_run(self, user, password):
        return user != None and password != None and os.getenv('VC_ATTACHMENT_BASE_PATH') != None and os.getenv('VC_ADMIN_ADDRESS') != None and os.getenv('VC_SMTP') != None and os.getenv('VC_SEND_ADDRESS') != None and os.getenv('VC_RECIPIENTS') != None

    def get_app_sandboxes(self, apps):
        for app in apps:
            app['sandboxes'] = self.sandboxes.get_sandboxes(app['app_id'])
    
    def get_app_sandbox_builds(self, apps):
        for app in apps:
            for sandbox in app['sandboxes']:
                sandbox['builds'] = self.builds.get_builds(app['app_id'], sandbox['sandbox_id'])

    def get_builds(self, apps):
        for app in apps:
            for sandbox in app['sandboxes']:
                for build in sandbox['builds']:
                    build['submitter'] = self.builds.get_build(app['app_id'], build['build_id'])

    def create_spreadsheet(self, apps):
        self.spreadsheet_creator.write_spreadsheet(apps)
    
    def send_message(self):
        if self.spreadsheet_creator.have_data:
            Mailer(os.getenv('VC_SEND_ADDRESS'), 
                os.getenv('VC_RECIPIENTS'), 
                constants.MESSAGE_SUBJECT, 
                os.getenv('VC_SMTP'), 
                25, 
                constants.BUILDS_FOUND_MESSAGE_TEXT.format(os.getenv('VC_ADMIN_ADDRESS')),
                self.spreadsheet_creator.filename)
        else:
            Mailer(os.getenv('VC_SEND_ADDRESS'), 
                os.getenv('VC_RECIPIENTS'), 
                constants.MESSAGE_SUBJECT, 
                os.getenv('VC_SMTP'), 
                25, 
                constants.BUILDS_NOT_FOUND_MESSAGE_TEXT.format(os.getenv('VC_ADMIN_ADDRESS')))

if __name__ == '__main__':
    app = App()
