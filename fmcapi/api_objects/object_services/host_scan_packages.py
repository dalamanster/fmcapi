"""Not yet implemented. First seen in v7.0 release of FMC API"""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class HostScanPackages(APIClassTemplate):
    """The HostScanPackages Object in the FMC."""

    FIRST_SUPPORTED_FMC_VERSION = "7.0"

    def post(self):
        """POST method for API for HostScanPackages not supported."""
        logging.info("POST method for API for HostScanPackages not supported.")
        pass

    def put(self):
        """PUT method for API for HostScanPackages not supported."""
        logging.info("PUT method for API for HostScanPackages not supported.")
        pass

    def delete(self):
        """DELETE method for API for HostScanPackages not supported."""
        logging.info("DELETE method for API for HostScanPackages not supported.")
        pass