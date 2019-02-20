# BT Smarthub Device List v.0.03

Python package allowing for a [BT Smart Hub 2] (https://www.productsandservices.bt.com/broadband/smart-hub/) router to be queried for devices.

The package will output either all devices stored in the router's memory or just the devices connected at present
as a list of dicts with the following keys:

### Installation
```sh
$ pip install btsmarthub2_devicelist
```

### Example

```sh
import btsmarthub2_devicelist
devicelist = btsmarthub2_devicelist.get_devicelist(router_ip='192.168.1.254', only_active_devices=True)
print(devicelist)
```

### Acknowledgments
This code is based on that created by jxwolstenholme project for the earlier version of the hub https://github.com/jxwolstenholme/btsmarthub_devicelist


