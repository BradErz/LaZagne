#!/usr/bin/env python
import os
import ConfigParser

from lazagne.config.write_output import print_debug
from lazagne.config.moduleInfo import ModuleInfo


class AWSCredentials(ModuleInfo):
    def __init__(self):
        options = {'command': '-a', 'action': 'store_true', 'dest': 'aws-creds', 'help': 'aws credentials'}
        ModuleInfo.__init__(self, 'AWS Credentials', 'sysadmin', options)

    def run(self, software_name=None):
        creds_found = []

        directory = "~/.aws"
        filename = "credentials"

        if 'AWS_SHARED_CREDENTIALS_FILE' in os.environ:
            path = os.environ['AWS_SHARED_CREDENTIALS_FILE']
        else:
            path = directory + '/' + filename

        full_path = os.path.expanduser(path)

        if os.path.exists(full_path) and os.path.getsize(full_path) > 0:

            config = ConfigParser.RawConfigParser()
            config.read(full_path)

            for section in config.sections():
                values = {}
                values['profile_name'] = section
                values['aws_access_key_id'] = config.get(section, "aws_access_key_id")
                values['aws_secret_access_key'] = config.get(section, "aws_secret_access_key")
                creds_found.append(values)

        return creds_found


