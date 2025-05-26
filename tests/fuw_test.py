import os
import unittest

from pymefuw import MEFUW

# Turn off sort so that tests run in line order
unittest.TestLoader.sortTestMethodsUsing = None

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
FUW_FOLDER_PATH = os.path.join(BASE_PATH, 'fuw')

class fuw_tests(unittest.TestCase):
    def setUp(self):
        self.ip_address = '192.168.40.123'
        pass

    def test_pvp6_v11(self):
        print('')
        self.fuw_helper_path = os.path.join(FUW_FOLDER_PATH, 'FUWhelper6xX.dll')
        self.fuw_image_path = os.path.join(FUW_FOLDER_PATH, 'SC_PVP6_v11.IMG')
        fuw = MEFUW(self.ip_address)
        fuw.upgrade(self.fuw_helper_path, self.fuw_image_path)

    def test_pvp6_v12(self):
        print('')
        self.fuw_helper_path = os.path.join(FUW_FOLDER_PATH, 'FUWhelper6xX.dll')
        self.fuw_image_path = os.path.join(FUW_FOLDER_PATH, 'SC_PVP6_v12.IMG')
        fuw = MEFUW(self.ip_address)
        fuw.upgrade(self.fuw_helper_path, self.fuw_image_path)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()