"""Not yet implemented. First seen in v7.0 release of FMC API"""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class IntrusionRules(APIClassTemplate):
    """The IntrusionRules Object in the FMC."""

    FIRST_SUPPORTED_FMC_VERSION = "7.0"