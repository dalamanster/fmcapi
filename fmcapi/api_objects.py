"""
This module contains the class objects that represent the various objects in the FMC.
"""

import logging
import datetime
import requests
from .helper_functions import *
from . import export

logging.debug("In the {} module.".format(__name__))


class Token(object):
    """
    The token is the validation object used with the FMC.

    """
    logging.debug("In the Token class.")

    MAX_REFRESHES = 3
    TOKEN_LIFETIME = 60 * 30
    API_PLATFORM_VERSION = 'api/fmc_platform/v1'

    def __init__(self, host='192.168.45.45', username='admin', password='Admin123', verify_cert=False):
        """
        Initialize variables used in the Token class.
        :param host:
        :param username:
        :param password:
        :param verify_cert:
        """
        logging.debug("In the Token __init__() class method.")

        self.__host = host
        self.__username = username
        self.__password = password
        self.verify_cert = verify_cert
        self.token_expiry = None
        self.token_refreshes = 0
        self.access_token = None
        self.uuid = None
        self.refresh_token = None
        self.generate_tokens()

    def generate_tokens(self):
        """
        Create new and refresh expired tokens.
        :return:
        """
        logging.debug("In the Token generate_tokens() class method.")

        if self.token_refreshes <= self.MAX_REFRESHES and self.access_token is not None:
            headers = {'Content-Type': 'application/json', 'X-auth-access-token': self.access_token,
                       'X-auth-refresh-token': self.refresh_token}
            url = 'https://{}/{}/auth/refreshtoken'.format(self.__host, self.API_PLATFORM_VERSION)
            logging.info("Refreshing tokens, {} out of {} refreshes, from {}.".format(self.token_refreshes,
                                                                                      self.MAX_REFRESHES, url))
            response = requests.post(url, headers=headers, verify=self.verify_cert)
            self.token_refreshes += 1
        else:
            headers = {'Content-Type': 'application/json'}
            url = 'https://{}/{}/auth/generatetoken'.format(self.__host, self.API_PLATFORM_VERSION)
            logging.info("Requesting new tokens from {}.".format(url))
            response = requests.post(url, headers=headers,
                                     auth=requests.auth.HTTPBasicAuth(self.__username, self.__password),
                                     verify=self.verify_cert)
            self.token_refreshes = 0
        self.access_token = response.headers.get('X-auth-access-token')
        self.refresh_token = response.headers.get('X-authrefresh-token')
        self.token_expiry = datetime.datetime.now() + datetime.timedelta(seconds=self.TOKEN_LIFETIME)
        self.uuid = response.headers.get('DOMAIN_UUID')

    def get_token(self):
        """
        Check validity of current token.  If needed make a new or resfresh.  Then return access_token.
        :return:
        """
        logging.debug("In the Token get_token() class method.")

        if datetime.datetime.now() > self.token_expiry:
            logging.info("Token Expired.")
            self.generate_tokens()
        return self.access_token


class FMCObject(object):
    """
    This class is the base framework for all the objects in the FMC.
    """

    REQUIRED_FOR_POST = ['name']
    REQUIRED_FOR_PUT = REQUIRED_FOR_POST.append('id')
    REQUIRED_FOR_DELETE = ['id']
    URL = None

    def __init__(self, fmc, **kwargs):
        logging.debug("In __init__() for fmc_object class.")
        self.fmc = fmc

    def parse_kwargs(self, **kwargs):
        if 'name' in kwargs:
            self.name = syntax_correcter(kwargs['name'])
        if 'description' in kwargs:
            self.description = kwargs['description']
        else:
            self.description = 'Created by fmcapi.'
        if 'metadata' in kwargs:
            self.metadata = kwargs['metadata']
        if 'value' in kwargs:
            self.value = kwargs['value']
        if 'overridable' in kwargs:
            self.overridable = kwargs['overridable']
        else:
            self.overridable = False
        if 'type' in kwargs:
            self.type = kwargs['type']
        if 'links' in kwargs:
            self.links = kwargs['links']
        if 'id' in kwargs:
            self.id = kwargs['id']

    def valid_for_post(self):
        logging.debug("In valid_for_post() for fmc_object class.")
        for item in self.REQUIRED_FOR_POST:
            if item not in self.__dict__:
                return False
        return True

    def post(self):
        logging.debug("In post() for fmc_object class.")
        if self.valid_for_post():
            response = self.fmc.send_to_api(method='post', url=self.URL, json_data=self.format_data())
            self.parse_kwargs(**response)
            return True
        else:
            logging.warning("post() method failed due to failure to pass valid_for_post() test.")
            return False

    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


@export
class HostObject(FMCObject):
    """
    The Host Object in the FMC.
    """

    URL = '/object/hosts'
    REQUIRED_FOR_POST = ['name', 'value']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for host_object class.")
        self.fmc = fmc
        self.parse_kwargs(**kwargs)
        if 'value' in kwargs:
            value_type = get_networkaddress_type(kwargs['value'])
            if value_type == 'range':
                logging.warning("value, {}, is of type {}.  Limited functionality for this object due to it being "
                                "created via the HostObject function.".format(kwargs['value'], value_type))
            if value_type == 'network':
                logging.warning("value, {}, is of type {}.  Limited functionality for this object due to it being "
                                "created via the HostObject function.".format(kwargs['value'], value_type))
            if validate_ip_bitmask_range(value=kwargs['value'], value_type=value_type):
                self.value = kwargs['value']
            else:
                logging.error("Provided value, {}, has an error with the IP address(es).".format(kwargs['value']))

    def format_data(self):
        logging.debug("In format_data() for host_object class.")
        json_data = {}
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'value' in self.__dict__:
            json_data['value'] = self.value
        if 'description' in self.__dict__:
            json_data['description'] = self.description
        return json_data
