from enum import StrEnum
from warnings import warn

from pymeu import comms
from pymeu import types
from pymeu import terminal

# Known functions available from FuwHelper.
class FuwHelperFunctions(StrEnum):
    CREATE_FOLDER = 'CreateRemDirectory' # Args: {Folder Path}, Returns: Static value if successful [Further investigation needed]
    DELETE_FILE = 'DeleteRemFile' # Args: {File Path}, Returns: ???
    GET_EXE_RUNNING = 'IsExeRunning' # Untested
    GET_FILE_EXISTS = 'FileExists' # Args: {File Path}, Returns: 1 if {File Path} exists
    GET_FOLDER_EXISTS = 'StorageExists' # Args: {Folder Path}, Returns: 1 if {Folder Path} exists
    STOP_PROCESS_ME = 'SafeTerminateME'

class MEFirmware(object):
    def __init__(self, comms_path: str, **kwargs):
        """
        Initializes an instance of the MEFirmware class.

        Args:
            comms_path (str): The path to the communications resource (ex: 192.168.1.20).
            **kwargs: Additional keyword arguments. 

                - driver (str): Optional; can be set to pycomm3 or pylogix
                to request specific driver for CIP messaging.
                - ignore_terminal_valid (bool): Optional; if set to True, 
                the instance will ignore terminal validation checks when
                performing uploads, downloads, etc.
                Defaults to False.
        """
        self.comms_path = comms_path
        self.driver = kwargs.get('driver', None)
        self.ignore_terminal_valid = kwargs.get('ignore_terminal_valid', False)

        warn('Forcing pylogix driver to be used while.  Pycomm3 socket timeout still under investigation.')
        self.driver = "pylogix"

    def upgrade(self, fuw_helper_path: str, fuw_image_path: str):
        with comms.Driver(self.comms_path, self.driver) as cip:
            # Increase socket timeout before process begins.
            # Doing this just before the firmware upgrade card transfer
            # seems to not work correctly.
            cip.timeout = 240

            # Validate device at this communications path is a terminal of known version.
            self.device = terminal.validation.get_terminal_info(cip)
            if not(terminal.validation.is_terminal_valid(self.device)):
                if self.ignore_terminal_valid:
                    warn('Invalid device selected, but terminal validation is set to IGNORE.')
                else:
                    raise Exception('Invalid device selected.  Use kwarg ignore_terminal_valid=True when initializing MEUtility object to proceed at your own risk.')

            # Download firmware upgrade wizard helper to terminal
            try:
                fuw_helper_file = types.MEFile('FUWhelper.dll',
                                            True,
                                            True,
                                            fuw_helper_path)
                resp = terminal.actions.download_file(cip, self.device, fuw_helper_file, '\\Storage Card')
                if not(resp):
                    self.device.log.append(f'Failed to upgrade terminal.')
                    return types.MEResponse(self.device, types.MEResponseStatus.FAILURE)
            except Exception as e:
                self.device.log.append(f'Exception: {str(e)}')
                self.device.log.append(f'Failed to upgrade terminal.')
                return types.MEResponse(self.device, types.MEResponseStatus.FAILURE)

            # Prepare terminal for firmware upgrade card
            try:
                fuw_helper = '\\Storage Card\\FUWhelper.dll'
                terminal.helper.run_function(cip, [fuw_helper, FuwHelperFunctions.GET_FILE_EXISTS, '\\Windows\\FUWhelper.dll'])
                terminal.helper.run_function(cip, [fuw_helper, FuwHelperFunctions.GET_FOLDER_EXISTS, '\\Storage Card\\vfs\\platform firmware'])
                terminal.helper.run_function(cip, [fuw_helper, FuwHelperFunctions.GET_FOLDER_EXISTS, '\\Storage Card'])
                terminal.helper.run_function(cip, [fuw_helper, FuwHelperFunctions.GET_FOLDER_EXISTS, '\\Storage Card\\vfs'])
                terminal.helper.run_function(cip, [fuw_helper, FuwHelperFunctions.CREATE_FOLDER, '\\Storage Card\\vfs'])
                terminal.helper.run_function(cip, [fuw_helper, FuwHelperFunctions.GET_FOLDER_EXISTS, '\\Storage Card\\vfs\\platform firmware'])
                terminal.helper.run_function(cip, [fuw_helper, FuwHelperFunctions.CREATE_FOLDER, '\\Storage Card\\vfs\\platform firmware'])
                terminal.helper.run_function(cip, [fuw_helper, FuwHelperFunctions.DELETE_FILE, '\\Storage Card\\Step2.dat'])
                terminal.helper.run_function(cip, [fuw_helper, FuwHelperFunctions.GET_EXE_RUNNING, 'MERuntime.exe'])
                terminal.helper.run_function(cip, [fuw_helper, FuwHelperFunctions.STOP_PROCESS_ME, ''])
                terminal.helper.run_function(cip, [fuw_helper, FuwHelperFunctions.GET_FILE_EXISTS, '\\Windows\\useroptions.txt'])
            except Exception as e:
                self.device.log.append(f'Exception: {str(e)}')
                self.device.log.append(f'Failed to upgrade terminal.')
                return types.MEResponse(self.device, types.MEResponseStatus.FAILURE)

            # Download firmware upgrade card to terminal
            try:
                fuw_image_file = types.MEFile('SC.IMG',
                                            True,
                                            True,
                                            fuw_image_path)
                resp = terminal.actions.download_file(cip, self.device, fuw_image_file, '\\vfs\\platform firmware')
                if not(resp):
                    self.device.log.append(f'Failed to upgrade terminal.')
                    return types.MEResponse(self.device, types.MEResponseStatus.FAILURE)
            except Exception as e:
                self.device.log.append(f'Exception: {str(e)}')
                self.device.log.append(f'Failed to upgrade terminal.')
                return types.MEResponse(self.device, types.MEResponseStatus.FAILURE)
            
        return types.MEResponse(self.device, types.MEResponseStatus.SUCCESS)