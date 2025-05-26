# pymefuw

PyMEFUW (Python ME Firmware Upgrade Wizard) is a high-risk, low-reward, experimental add-on to PyMEU (Python ME Utility).<br>
Use at your own risk.<br>

## Basic Examples

Use the upgrade function to apply a firmware upgrade card to the remote terminal:

```python
from pymefuw import MEUFUW
fuw = MEUFUW('YourPanelViewIpAddress')
fuw.upgrade('PathToHelper', 'PathToImage')
```