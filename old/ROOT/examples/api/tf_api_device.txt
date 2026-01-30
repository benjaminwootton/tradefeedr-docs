###############################################################################
# tf_api_device(v1) - REST Api Client with Auth0 Device Code Authentication
###############################################################################
# - see https://auth0.com/docs/flows/device-authorization-flow


from collections import OrderedDict

import requests
import urllib3
import os

###############################################################################
# Config / Settings
###############################################################################


# Tradefeedr / REST Api url
TRADEFEEDR_API_URL = "https://api.tradefeedr.com"

# Auth0 / Settings / Tenant
_AUTH0_TENANT_URL = "https://tradefeedr.eu.auth0.com"

# Auth0 / Applications / Native - Client ID
_AUTH0_NATIVE_APP_CLIENT_ID = "vzsxt6b2Sv0FvORpCzf1EbwvvWBEhFK9"

# Auth0 / APIs / Custom Api - API Audience
_AUTH0_REST_API_AUDIENCE = "https://api.tradefeedr.com"

# Whether to verify SSL certificates on https requests
_VERIFY_CERTIFICATES = True

# Auth0 device code request endpoint
_AUTH0_DEVICE_CODE_URL = "/".join([_AUTH0_TENANT_URL, "oauth/device/code"])

# Auth0 token request endpoint
_AUTH0_TOKEN_URL = "/".join([_AUTH0_TENANT_URL, "oauth/token"])

# Tradefeedr / default scopes
_TRADEFEEDR_DEFAULT_SCOPES = ["tfapi:client"]

if "__file__" in dir():
    _ACCESS_TOKEN_PATH = os.path.dirname(__file__) + "/" + "tradefeedr_access_token.txt"
else:
    _ACCESS_TOKEN_PATH = "./" + "tradefeedr_access_token.txt"


###############################################################################
# Public Functions / Classes
###############################################################################


class TfApiDevice():
    """
    Usage:
        0.) Create object tf_api_object = TfApiDevice()
        1.) Call tf_api_object.request_login()
            - will return a map containing user authentication url
        2.) Visit the url provided by 1.) in a web browser and authenticate
        3.) Call tf_api_object.request_token()
            - will return a map containing a valid access token
        4.) Call tf_api_object.query_api(endpoint="", options={}) function to use api
    """

    _access_token_path = _ACCESS_TOKEN_PATH
    _state = {}

    def _send_request_for_login(self, scopes):
        """
        Function to send request for device/user codes and verification uri from Auth0
        Parameters:
            scopes (list): List of scope strings to request access for
        Returns:
            dict: Map containing "device_code", "user_code" and "verification_uri" plus activation query limits
        """
        json_request = {
            "client_id": _AUTH0_NATIVE_APP_CLIENT_ID,
            "scope": " ".join(scopes),
            "audience": _AUTH0_REST_API_AUDIENCE
        }
        response = requests.post(_AUTH0_DEVICE_CODE_URL, headers={}, json=json_request)
        response.raise_for_status()
        return response.json()

    def _send_request_for_token(self, device_code):
        """
        Function to send request for valid "access_token" and activate this script as a device
        Parameters:
            device_code (str): Recent device code received from device code request
        Returns:
            dict: Map containing "access_token", "refresh_token", "id_token" and expiry information
        """
        json_request = {
            "client_id": _AUTH0_NATIVE_APP_CLIENT_ID,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "device_code": device_code
        }
        response = requests.post(_AUTH0_TOKEN_URL, headers={}, json=json_request)
        response.raise_for_status()
        return response.json()

    def request_login(self, scopes=None):
        """
        Function to request device/user codes and verification uri from Auth0
        Parameters:
            scopes (list): List of scope strings to request access for
        Returns:
            dict: Map containing "verification_uri_complete"
        """
        if scopes is None:
            scopes = _TRADEFEEDR_DEFAULT_SCOPES
        print("Requesting login...")
        self._state = self._send_request_for_login(scopes)
        return {k: self._state[k] for k in ("verification_uri_complete",) if k in self._state}

    def request_token(self):
        """
        Function to request token ( after user authenticated in web browser )
        Returns:
            dict: Map containing "access_token"
        """
        print("Requesting access token...")
        if "device_code" not in self._state:
            raise Exception("No 'device_code' found : Please run request_login()")
        self._state.update(self._send_request_for_token(self._state["device_code"]))
        self._state.pop("device_code")
        return {k: self._state[k] for k in ("access_token",) if k in self._state}

    def export_token(self):
        access_token = self._state["access_token"]
        with open(self._access_token_path, "w") as file:
            file.write(access_token)
        return access_token

    def import_token(self, access_token=None):
        if access_token is None:
            with open(self._access_token_path, "r") as file:
                access_token = file.readlines()[0]
        self._state["access_token"] = access_token
        return access_token

    def query_api(self, endpoint="test_success", options=None, raise_for_status=True):
        """
        Function to call the Tradefeedr REST api
        Parameters:
            endpoint (str): Name of remote endpoint to call
            options (any): Any valid options for "endpoint"
            raise_for_status (bool) Whether to raise an error based on status in returned message
        Returns:
            dict: Map containing json results of api called
        """
        if options is None:
            options = dict()
        print("Querying api...")
        if "access_token" not in self._state:
            raise Exception(
                "No 'access_token' found : Please run request_login(), authenticate and run request_token()")
        rest_headers = {"Authorization": "Bearer " + self._state["access_token"]}
        json_request = {"options": options}
        response = requests.post(TRADEFEEDR_API_URL + "/client/" + endpoint, headers=rest_headers, json=json_request,
                                 verify=_VERIFY_CERTIFICATES)
        if raise_for_status:
            response.raise_for_status()
        return response.json(object_pairs_hook=OrderedDict)


###############################################################################
# Initialise
###############################################################################


if not _VERIFY_CERTIFICATES:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
