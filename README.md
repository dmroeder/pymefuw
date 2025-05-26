# pymefuw

PyMEFUW (Python ME Firmware Upgrade Wizard) is a high-risk, low-reward, extremely-experimental add-on to PyMEU (Python ME Utility).<br>
It is for research purposes only.<br>

## Basic Examples

Use the upgrade function to apply a firmware upgrade card to the remote terminal:

```python
from pymefuw import MEFirmware
fuw = MEFirmware('YourPanelViewIpAddress')
fuw.upgrade('PathToHelper', 'PathToImage')
```