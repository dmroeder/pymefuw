# pymefuw

PyMEFUW (Python ME Firmware Upgrade Wizard) is a high-risk, low-reward, experimental add-on to PyMEU (Python ME Utility).  Use at your own risk.<br>

## Basic Examples

Use the upgrade function to transfer an unpacked firmware image to the remote terminal:

```python
from pymefuw import MEUFUW
fuw = MEUFUW('YourPanelViewIpAddress')
fuw.upgrade('PathToHelper', 'PathToImage')
```