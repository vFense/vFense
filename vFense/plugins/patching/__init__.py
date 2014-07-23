import logging, logging.config
from vFense import VFENSE_LOGGING_CONFIG
from vFense.core._constants import CommonKeys
from vFense.core.results import ApiResultKeys
from vFense.plugins.patching._constants import (
    AppDefaults, PossibleRebootValues, PossibleHiddenValues,
    CommonSeverityKeys, FileDefaults
)
from vFense.plugins.patching._db_model import (
    DbCommonAppKeys, FilesKey
)

from vFense.plugins.patching.status_codes import (
    PackageCodes
)

logging.config.fileConfig(VFENSE_LOGGING_CONFIG)
logger = logging.getLogger('rvapi')

class Apps(object):
    """Used to represent an instance of an app."""

    def __init__(self, name=None, version=None, arch=None, app_id=None,
                 kb=None, support_url=None, vendor_severity=None,
                 vfense_severity=None, os_code=None,
                 os_string=None, vendor=None, description=None,
                 cli_options=None, release_date=None,
                 reboot_required=None, hidden=None, update=None,
                 download_status=None, vulnerability_id=None,
                 vulnerability_categories=None, cve_ids=None):
        """
        Kwargs:
            name (str): Name of the application.
            version (str): Current version of the application.
            arch (int): 64 or 32.
            app_id (str): The primary key of this application.
            support_url (str): The vendor supplied url.
            vendor_severity (str): This is the vendor supplied severity.
            vfense_severity (str): Optional, Recommended, or Critical
            os_code (str): windows, linux, or darwin
            os_string (str): CentOS 6.5, Ubuntu 12.0.4, etc...
            vendor (str): The vendor, this application belongs too.
            description (str): The description of this application.
            cli_options (str): Options to be passed while installing this
                application.
            release_date (float): The Unix timestamp aka epoch time.
            reboot_required (str): possible, required, none
            hidden (str): no or yes.
            update (int): The integer status code that represents if this
                application is a new install or an update.
            download_status (int): The integer status code that represents
                if this application has been downlaoded successfully.
        """
        self.name = name
        self.version = version
        self.arch = arch
        self.app_id = app_id
        self.kb = kb
        self.support_url = support_url
        self.vendor_severity = vendor_severity
        self.vfense_severity = vfense_severity
        self.os_code = os_code
        self.os_string = os_string
        self.vendor = vendor
        self.description = description
        self.cli_options = cli_options
        self.release_date = release_date
        self.reboot_required = reboot_required
        self.hidden = hidden
        self.update = update
        self.download_status = download_status
        self.vulnerability_id = vulnerability_id
        self.vulnerability_categories = vulnerability_categories
        self.cve_ids = cve_ids

    def fill_in_defaults(self):
        """Replace all the fields that have None as their value with
        the hardcoded default values.

        Use case(s):
            Useful when you want to create an install instance and only
            want to fill in a few fields, then allow the install
            functions to call this method to fill in the rest.
        """

        if not self.hidden:
            self.hidden = AppDefaults.HIDDEN

        if not self.reboot_required:
            self.reboot_required= AppDefaults.REBOOT_REQUIRED

        if not self.update:
            self.update = AppDefaults.UPDATE

        if not self.download_status:
            self.download_status = AppDefaults.DOWNLOAD_STATUS

        if not self.vfense_severity:
            self.vfense_severity = AppDefaults.VFENSE_SEVERITY


    def get_invalid_fields(self):
        """Check the app for any invalid fields.

        Returns:
            (list): List of key/value pair dictionaries corresponding
                to the invalid fields.

                Ex:
                    [
                        {'view_name': 'the invalid name in question'},
                        {'net_throttle': -10}
                    ]
        """
        invalid_fields = []

        if self.name:
            if len(self.name) <= 1:
                invalid_fields.append(
                    {
                        DbCommonAppKeys.Name: self.name,
                        CommonKeys.REASON: (
                            '{0} not a valid application name'
                            .format(self.name)
                        ),
                        ApiResultKeys.VFENSE_STATUS_CODE: (
                            PackageCodes.InvalidValue
                        )
                    }
                )

        if self.version:
            if len(self.version) <= 1:
                invalid_fields.append(
                    {
                        DbCommonAppKeys.Version: self.version,
                        CommonKeys.REASON: (
                            '{0} not a valid application version'
                            .format(self.version)
                        ),
                        ApiResultKeys.VFENSE_STATUS_CODE: (
                            PackageCodes.InvalidValue
                        )
                    }
                )

        if self.reboot_required:
            if (self.reboot_required not
                    in PossibleRebootValues.get_reboot_values()):
                invalid_fields.append(
                    {
                        DbCommonAppKeys.RebootRequired: self.reboot_required,
                        CommonKeys.REASON: (
                            '{0} not a valid reboot value'
                            .format(self.reboot_required)
                        ),
                        ApiResultKeys.VFENSE_STATUS_CODE: (
                            PackageCodes.InvalidValue
                        )
                    }
                )


        if self.hidden:
            if (self.hidden not
                    in PossibleHiddenValues.get_hidden_values()):
                invalid_fields.append(
                    {
                        DbCommonAppKeys.Hidden: self.hidden,
                        CommonKeys.REASON: (
                            '{0} not a valid hidden value'
                            .format(self.hidden)
                        ),
                        ApiResultKeys.VFENSE_STATUS_CODE: (
                            PackageCodes.InvalidValue
                        )
                    }
                )

        if self.release_date:
            if not isinstance(self.release_date, float):
                invalid_fields.append(
                    {
                        DbCommonAppKeys.ReleaseDate: self.release_date,
                        CommonKeys.REASON: (
                            '{0} not a valid release date'
                            .format(self.release_date)
                        ),
                        ApiResultKeys.VFENSE_STATUS_CODE: (
                            PackageCodes.InvalidValue
                        )
                    }
                )


        if self.vfense_severity:
            if (self.vfense_severity not
                    in CommonSeverityKeys.get_valid_severities()):
                invalid_fields.append(
                    {
                        DbCommonAppKeys.Hidden: self.hidden,
                        CommonKeys.REASON: (
                            '{0} not a valid vfense severity'
                            .format(self.vfense_severity)
                        ),
                        ApiResultKeys.VFENSE_STATUS_CODE: (
                            PackageCodes.InvalidValue
                        )
                    }
                )


        return invalid_fields

    def to_dict(self):
        """ Turn the view fields into a dictionary.

        Returns:
            (dict): A dictionary with the fields corresponding to the
                install operation.

        """

        return {
            DbCommonAppKeys.AppId: self.app_id,
            DbCommonAppKeys.Name: self.name,
            DbCommonAppKeys.Hidden: self.hidden,
            DbCommonAppKeys.Description: self.description,
            DbCommonAppKeys.ReleaseDate: self.release_date,
            DbCommonAppKeys.RebootRequired: self.reboot_required,
            DbCommonAppKeys.Kb: self.kb,
            DbCommonAppKeys.SupportUrl: self.support_url,
            DbCommonAppKeys.Version: self.version,
            DbCommonAppKeys.OsCode: self.os_code,
            DbCommonAppKeys.OsStrings: [self.os_string],
            DbCommonAppKeys.vFenseSeverity: self.vfense_severity,
            DbCommonAppKeys.VendorSeverity: self.vendor_severity,
            DbCommonAppKeys.VendorName: self.vendor_name,
            DbCommonAppKeys.FilesDownloadStatus: self.download_status,
            DbCommonAppKeys.VulnerabilityId: self.vulnerability_id,
            DbCommonAppKeys.VulnerabilityCategories: (
                self.vulnerability_categories
            ),
            DbCommonAppKeys.CveIds: self.cve_ids
        }

    def to_dict_non_null(self):
        """ Use to get non None fields of an install. Useful when
        filling out just a few fields to perform an install.

        Returns:
            (dict): a dictionary with the non None fields of this install.
        """
        install_dict = self.to_dict()

        return {k:install_dict[k] for k in install_dict
                if install_dict[k] != None}



class Files(object):
    """Used to represent an instance of an app."""

    def __init__(self, file_name=None, file_hash=None, file_size=None,
                 download_url=None, app_ids=None, agent_ids=None):
        """
        Kwargs:
            file_name (str): Name of the file.
            file_hash (str): The md54 hash of the file.
            file_size (int): Size of the file in kb.
            download_url (str): The url where this file can be downloaded from.
            app_ids (list): The application ids, this file is associated with.
            agent_ids (list): The agent ids this file is associated with.
        """
        self.name = file_name
        self.file_hash = file_hash
        self.size = file_size
        self.download_url = download_url
        self.app_ids = app_ids
        self.agent_ids = agent_ids

    def fill_in_defaults(self):
        """Replace all the fields that have None as their value with
        the hardcoded default values.

        Use case(s):
            Useful when you want to create an install instance and only
            want to fill in a few fields, then allow the install
            functions to call this method to fill in the rest.
        """

        if not self.agent_ids:
            self.agent_ids = FileDefaults.AGENT_IDS

        if not self.app_ids:
            self.app_ids= FileDefaults.APP_IDS

    def get_invalid_fields(self):
        """Check the app for any invalid fields.

        Returns:
            (list): List of key/value pair dictionaries corresponding
                to the invalid fields.

                Ex:
                    [
                        {'view_name': 'the invalid name in question'},
                        {'net_throttle': -10}
                    ]
        """
        invalid_fields = []

        if self.file_name:
            if len(self.file_name) <= 1:
                invalid_fields.append(
                    {
                        FilesKey.FileName: self.file_name,
                        CommonKeys.REASON: (
                            '{0} not a valid file name'
                            .format(self.file_name)
                        ),
                        ApiResultKeys.VFENSE_STATUS_CODE: (
                            PackageCodes.InvalidValue
                        )
                    }
                )

        if self.file_size:
            if not int(self.file_size):
                invalid_fields.append(
                    {
                        FilesKey.FileSize: self.file_size,
                        CommonKeys.REASON: (
                            '{0} not a valid file size'
                            .format(self.file_size)
                        ),
                        ApiResultKeys.VFENSE_STATUS_CODE: (
                            PackageCodes.InvalidValue
                        )
                    }
                )

        if self.file_hash:
            if len(self.file_has) <= 1:
                invalid_fields.append(
                    {
                        FilesKey.FileHash: self.file_hash,
                        CommonKeys.REASON: (
                            '{0} not a valid hash'
                            .format(self.file_hash)
                        ),
                        ApiResultKeys.VFENSE_STATUS_CODE: (
                            PackageCodes.InvalidValue
                        )
                    }
                )

        if self.app_ids:
            if not isinstance(self.app_ids, list):
                invalid_fields.append(
                    {
                        FilesKey.AppIds: self.app_ids,
                        CommonKeys.REASON: (
                            '{0} not a valid list'
                            .format(self.app_ids)
                        ),
                        ApiResultKeys.VFENSE_STATUS_CODE: (
                            PackageCodes.InvalidValue
                        )
                    }
                )

        if self.agent_ids:
            if not isinstance(self.agent_ids, list):
                invalid_fields.append(
                    {
                        FilesKey.AgentIds: self.agent_ids,
                        CommonKeys.REASON: (
                            '{0} not a valid list'
                            .format(self.agent_ids)
                        ),
                        ApiResultKeys.VFENSE_STATUS_CODE: (
                            PackageCodes.InvalidValue
                        )
                    }
                )

        if self.download_url:
            if len(self.download_url) <= 1:
                invalid_fields.append(
                    {
                        FilesKey.FileUri: self.download_url,
                        CommonKeys.REASON: (
                            '{0} not a valid url'
                            .format(self.download_url)
                        ),
                        ApiResultKeys.VFENSE_STATUS_CODE: (
                            PackageCodes.InvalidValue
                        )
                    }
                )

        return invalid_fields

    def to_dict(self):
        """ Turn the view fields into a dictionary.

        Returns:
            (dict): A dictionary with the fields corresponding to the
                install operation.

        """

        return {
            FilesKey.FileName: self.file_name,
            FilesKey.AppIds: self.app_ids,
            FilesKey.AgentIds: self.agent_ids,
            FilesKey.Uri: self.download_url,
            FilesKey.FileHash: self.file_hash,
            FilesKey.FileSize: self.file_size,
        }

    def to_dict_non_null(self):
        """ Use to get non None fields of an install. Useful when
        filling out just a few fields to perform an install.

        Returns:
            (dict): a dictionary with the non None fields of this install.
        """
        install_dict = self.to_dict()

        return {k:install_dict[k] for k in install_dict
                if install_dict[k] != None}
