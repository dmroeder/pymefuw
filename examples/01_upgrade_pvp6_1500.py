# First use the ME Firmware Upgrade wizard to create a Firmware Update Card in a folder on your computer.
# Then run this code to transfer the SC.IMG file it generates to the remote terminal.
#
# This example is specifically for a PanelView Plus 6 1500.
#
from pymefuw import MEFirmware
fuw = MEFirmware('YourPanelViewIpAddress')
fuw.upgrade('C:\\Program Files (x86)\\Rockwell Software\\RSView Enterprise\\FUWhelper6xX.dll','C:\\ExampleFirmwareUpdateCard\\upgrade\\SC.IMG')