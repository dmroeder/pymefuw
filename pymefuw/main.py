import time
from warnings import warn

from pymeu import comms
from pymeu import terminal
from pymeu import types
from pymefuw.terminal import fuwhelper

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
            # Set socket timeout first.
            # The terminal will pause at certain points and delay acknowledging messages.
            # Without this, the process will fail and the terminal will require a factory reset.
            cip.timeout = 255

            # Validate device at this communications path is a terminal of known version.
            self.device = terminal.validation.get_terminal_info(cip)
            if not(terminal.validation.is_terminal_valid(self.device)):
                if self.ignore_terminal_valid:
                    warn('Invalid device selected, but terminal validation is set to IGNORE.')
                else:
                    raise Exception('Invalid device selected.  Use kwarg ignore_terminal_valid=True when initializing MEUtility object to proceed at your own risk.')

            # Determine if firmware upgrade helepr exists already
            if terminal.helper.get_file_exists(cip, self.device.paths, '\\Windows\\FUWhelper.dll'):
                transfer_fuwhelper = False
                self.device.paths.fuw_helper_file = '\\Windows\\FUWhelper.dll'
                self.device.log.append(f'Firmware upgrade helper already present on terminal.')
            else:
                transfer_fuwhelper = True
                self.device.paths.fuw_helper_file = '\\Storage Card\\FUWhelper.dll'
                self.device.log.append(f'Firmware upgrade helper not present on terminal, will transfer.')
  
            # Download firmware upgrade wizard helper to terminal
            if transfer_fuwhelper:
                try:
                    fuw_helper_file = types.MEFile('FUWhelper.dll',
                                                True,
                                                True,
                                                fuw_helper_path)
                    resp = terminal.actions.download_file(cip, self.device, fuw_helper_file, '\\Storage Card')
                    if not(resp):
                        self.device.log.append(f'Failed to upgrade terminal.')
                        return types.MEResponse(self.device, types.MEResponseStatus.FAILURE)
                    
                    time.sleep(10)
                except Exception as e:
                    self.device.log.append(f'Exception: {str(e)}')
                    self.device.log.append(f'Failed to upgrade terminal.')
                    return types.MEResponse(self.device, types.MEResponseStatus.FAILURE)

            # Prepare terminal for firmware upgrade card
            try:
                fuwhelper.get_file_exists(cip, self.device.paths, '\\Windows\\FUWhelper.dll')

                if not(fuwhelper.get_folder_exists(cip, self.device.paths, '\\Storage Card')):
                    fuwhelper.create_folder(cip, self.device.paths, '\\Storage Card')
                if not(fuwhelper.get_folder_exists(cip, self.device.paths, '\\Storage Card\\vfs')):
                    fuwhelper.create_folder(cip, self.device.paths, '\\Storage Card\\vfs')
                if not(fuwhelper.get_folder_exists(cip, self.device.paths, '\\Storage Card\\vfs\\platform firmware')):
                    fuwhelper.create_folder(cip, self.device.paths, '\\Storage Card\\vfs\\platform firmware')

                fuwhelper.delete_file(cip, self.device.paths, '\\Storage Card\\Step2.dat')
                if fuwhelper.get_exe_running(cip, self.device.paths, 'MERuntime.exe'):
                    fuwhelper.stop_process_me(cip, self.device.paths)

                fuwhelper.get_file_exists(cip, self.device.paths, '\\Windows\\useroptions.txt')
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