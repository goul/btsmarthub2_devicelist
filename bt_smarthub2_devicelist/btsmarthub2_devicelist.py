
import urllib.request
from urllib.error import HTTPError, URLError
from socket import timeout

import re
import json
import logging


_LOGGER = logging.getLogger(__name__)


# Hub uri for getting device list
HUB_DEVICE_URI='/cgi/cgi_basicMyDevice.js'

# identifier for line that contains the actual device information from the hub
DEVICE_TOKEN='var known_device_list='

# list of labels for each device
DEVICE_LABELS=[
    "mac",
    "hostname",
    "ip",
    "ipv6",
    "name",
    "activity",
    "os",
    "device",
    "time_first_seen",
    "time_last_active",
    "dhcp_option",
    "port",
    "ipv6_ll",
    "activity_ip",
    "activity_ipv6_ll",
    "activity_ipv6",
    "device_oui",
    "device_serial",
    "device_class",
    "reconnected"
    ]





# string replace to quote all the labels to make it json compliant
def updateLabel(source,labels):
    # sort so we do larges matches first removing issues on thinhs like 'ip' used in longer strings
    labels.sort(key=len, reverse=True)
    for label in labels:
        source=source.replace(label+":", "\""+label+"\":")

    return source


def get_devicelist(router_ip='192.168.1.254', only_active_devices=False):

    request_url= 'http://' + router_ip + HUB_DEVICE_URI

    # Read the URL from hub and unquote the strings
    try:
        body = urllib.request.urlopen(request_url, timeout=10).read().decode('utf-8')
        body=urllib.parse.unquote(body)
    except (HTTPError, URLError) as error:
        _LOGGER.error('Unable to read from hub as  %s\nURL: %s', error, request_url)
    except timeout:
        _LOGGER.error('socket timed out - URL %s', request_url)
    else:
        _LOGGER.info('Access successful.')

    # and remove all newlines
    body = body.replace("\n","")

    # pull out the javascript line from the whole file
    searchLine=re.search(r'known_device_list=(.+?),null',body);

    # my regexx strips the close of the list
    javascriptArraySingleQuotes=searchLine.group(1)+']';

    # to allow json to read this, add quotes around the item labels.
    javascriptArraySingleQuotes=updateLabel(javascriptArraySingleQuotes,DEVICE_LABELS);

    # change the strings to boolean for '0' and '1'
    javascriptArraySingleQuotes=javascriptArraySingleQuotes.replace("'1'","true")
    javascriptArraySingleQuotes=javascriptArraySingleQuotes.replace("'0'", "false");


    # json likes double not single quotes
    javascriptArray=javascriptArraySingleQuotes.replace("'","\"")

    # map to the old field names to keep compatibility with other version of hub
    javascriptArray=javascriptArray.replace("\"mac\"","\"PhysAddress\"")
    javascriptArray = javascriptArray.replace("\"activity\"", "\"Active\"")
    javascriptArray = javascriptArray.replace("\"hostname\"", "\"UserHostName\"")
    javascriptArray = javascriptArray.replace("\"ip\"", "\"IPAddress\"")


    print(javascriptArray)
    # read into obj model using json
    deviceData=json.loads(javascriptArray)

    # shrink them down
    deviceData=parse_devicelist(deviceData)

    # filter when asked
    if only_active_devices:
        return [device for device in deviceData if device.get('Active') == '1']

    return deviceData;


# Filter down to just the same fields as the original library
def parse_devicelist(device_list):
    keys = {'UserHostName', 'PhysAddress', 'IPAddress', 'Active'}
    devices = [{k: v for k, v in i.items() if k in keys} for i in device_list]

    return devices




# # Some testing
# print("Only active")
# devices=get_devicelist("192.168.1.254",True)
#
# for device in devices:
#     print( device.get('Active') , device.get('UserHostName'),device.get('PhysAddress'))
#
#
# print("All")
# devices = get_devicelist("192.168.1.254")
#
# for device in devices:
#         print( device.get('Active') , device.get('UserHostName'),device.get('PhysAddress'))
#         print(device)
#
#
#
#
# #
# # import time
# #
# # while True :
# #     devices = get_devicelist("192.168.1.254", True)
# #     for device in devices:
# #         if device.get('hostname') == 'iPhone-PG' :
# #             print ("PG phone connected")
# #
# #
# #     print (".")
# #
# #     time.sleep(5)


