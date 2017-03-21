#!/usr/bin/env python
import os
import ConfigParser

from lazagne.config.write_output import print_debug
from lazagne.config.constant import *
from lazagne.config.moduleInfo import ModuleInfo


class AWSCredentials(ModuleInfo):
    def __init__(self):
        options = {'command': '-a', 'action': 'store_true', 'dest': 'aws-creds', 'help': 'aws credentials'}
        ModuleInfo.__init__(self, 'AWS Credentials', 'sysadmin', options)

    def check_env_vars(self):
        if os.environ.get('AWS_ACCESS_KEY_ID') and os.environ.get('AWS_SECRET_ACCESS_KEY'):
            values = {}
            values['aws_access_key_id'] = os.environ.get('AWS_ACCESS_KEY_ID')
            values['aws_secret_access_key'] = os.environ.get('AWS_SECRET_ACCESS_KEY')
            return values
        else:
            return None

    def check_creds_file(self):
        profiles = []
        directory = constant.profile['USERPROFILE'] + "\\.aws"
        filename = "credentials"

        if os.environ.get('AWS_SHARED_CREDENTIALS_FILE'):
            path = os.environ['AWS_SHARED_CREDENTIALS_FILE']
        else:
            path = directory + '' + filename

        full_path = os.path.expanduser(path)

        if os.path.exists(full_path) and os.path.getsize(full_path) > 0:

            config = ConfigParser.RawConfigParser()
            config.read(full_path)

            for section in config.sections():
                values = {}
                values['profile_name'] = section
                values['aws_access_key_id'] = config.get(section, "aws_access_key_id")
                values['aws_secret_access_key'] = config.get(section, "aws_secret_access_key")
                profiles.append(values)

        return profiles

    def run(self, software_name=None):
        creds_found = []

        access_keys_from_envvar = self.check_env_vars()
        if access_keys_from_envvar:
            creds_found.append(access_keys_from_envvar)


        access_keys_from_creds_file = self.check_creds_file()
        if access_keys_from_creds_file:
            for profile in access_keys_from_creds_file:
                print(profile)
                creds_found.append(profile)

        return creds_found


