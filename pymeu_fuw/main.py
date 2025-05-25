import time

from pymeu import comms
from pymeu import types
from pymeu.terminal import files
from pymeu.terminal import helper

class MEFUW(object):
    def __init__(self, comms_path: str, **kwargs):
        self.comms_path = comms_path
        self.driver = "pylogix"

    def upgrade(self, fuw_helper_path: str, fuw_image_path: str):
        with comms.Driver(self.comms_path, self.driver) as cip:
            cip.timeout = 240

            # Phase 1 - Send firmware upgrade wizard helper
            get_unk1 = files.is_get_unk_valid(cip)
            fuw_helper_file = types.MEFile('FUWhelper.dll',
                                           True,
                                           True,
                                           fuw_helper_path)
            
            transfer_instance = files.create_transfer_instance_download(cip, fuw_helper_file, '\\Storage Card')
            set_unk1 = files.is_set_unk_valid(cip)

            with open(fuw_helper_path, 'rb') as source_file:
                files.download(cip, transfer_instance, bytearray(source_file.read()))
            
            files.delete_transfer_instance(cip, transfer_instance)
            time.sleep(15)

            # Phase 2 - Send firmware upgrade image
            fuw_helper = '\\Storage Card\\FUWhelper.dll'
            helper.run_function(cip, [fuw_helper, 'FileExists', '\\Windows\\FUWhelper.dll'])
            helper.run_function(cip, [fuw_helper, 'StorageExists', '\\Storage Card\\vfs\\platform firmware'])
            helper.run_function(cip, [fuw_helper, 'StorageExists', '\\Storage Card'])
            helper.run_function(cip, [fuw_helper, 'StorageExists', '\\Storage Card\\vfs'])
            helper.run_function(cip, [fuw_helper, 'CreateRemDirectory', '\\Storage Card\\vfs'])
            helper.run_function(cip, [fuw_helper, 'StorageExists', '\\Storage Card\\vfs\\platform firmware'])
            helper.run_function(cip, [fuw_helper, 'CreateRemDirectory', '\\Storage Card\\vfs\\platform firmware'])
            helper.run_function(cip, [fuw_helper, 'DeleteRemFile', '\\Storage Card\\Step2.dat'])
            helper.run_function(cip, [fuw_helper, 'IsExeRunning', 'MERuntime.exe'])
            helper.run_function(cip, [fuw_helper, 'SafeTerminateME', ''])
            helper.run_function(cip, [fuw_helper, 'FileExists', '\\Windows\\useroptions.txt'])

            get_unk1 = files.is_get_unk_valid(cip)
            fuw_image_file = types.MEFile('SC.IMG',
                                           True,
                                           True,
                                           fuw_image_path)
            
            transfer_instance = files.create_transfer_instance_download(cip, fuw_image_file, '\\vfs\\platform firmware')
            set_unk1 = files.is_set_unk_valid(cip)
            with open(fuw_image_path, 'rb') as source_file:
                files.download(cip, transfer_instance, bytearray(source_file.read()))
                
            files.delete_transfer_instance(cip, transfer_instance)