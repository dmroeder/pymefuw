# pymeu-fuw

PyMEU-FUW (Python ME Utility Firmware Upgrade Wizard) is a high-risk, low-reward, experimental add-on to PyMEU.  Use at your own risk.<br>

## Basic Examples

Use the upgrade function to transfer an unpacked firmware image to the remote terminal:

```python
from pymeu_fuw import MEUFUW
fuw = MEUFUW('YourPanelViewIpAddress')
meu.upgrade('PathToHelper', 'PathToImage')
```