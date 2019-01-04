"""
Logger module for outputting text to console
"""

from termcolor import colored

class Logger(object):
    def __init__(self):
        return

    def info(self, message):
        self.output('[+]', message, 'green')

    def error(self, message):
        self.output('[-]', message, 'red')

    def exception(self, message):
        self.output('[*]', message, 'red')

    def output(self, prefix, message, color):
        print(colored('{} - {}'.format(prefix, message), color))
