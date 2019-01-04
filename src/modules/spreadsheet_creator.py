"""
Wrapper modules for xslxwriter implementation
"""
import os
import xlsxwriter
from datetime import date

class SpreadsheetCreator(object):
    def __init__(self):
        self.have_data = False
        self.filename = '{}VeracodeSandboxResults-{}.xlsx'.format(os.getenv('VC_ATTACHMENT_BASE_PATH'), date.today())
        return
    
    def write_spreadsheet(self, apps):
        workbook = xlsxwriter.Workbook(self.filename)
        worksheet = workbook.add_worksheet('Aggregated Build Data')
        bold = workbook.add_format({'bold': True})
        worksheet.write('A1', 'User', bold)
        worksheet.write('B1', 'Total Builds', bold)
        row = 1
        col = 0
        data = {}

        for app in apps:
            for sandbox in app['sandboxes']:
                for build in sandbox['builds']:
                    if not build['submitter'] in data:
                        data[build['submitter']] = 0
                    data[build['submitter']] += 1
        if(len(data) > 0):
            self.have_data = True
        for user, number_of_builds in data.items():
            worksheet.write(row, col, user)
            worksheet.write(row, col + 1, number_of_builds)
            row += 1

        workbook.close()