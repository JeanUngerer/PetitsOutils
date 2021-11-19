#! /usr/bin/env python3

# python decode.py puqrcovid.txt puqrcovid.jpg

# python -m pip uninstall pillow
# python -m pip uninstall pyzbar
# pip install base45 cbor2
# pip install pillow pyzbar
# pip install cose
# pip install python-barcode
# pip install qrcode

import json
import sys
import zlib
 
import base45
import cbor2
from cose.messages import CoseMessage

import pprint
import cbor2

# http://zbar.sourceforge.net/download.html
# https://pypi.org/project/pyzbar/
# https://www.microsoft.com/en-US/download/details.aspx?id=40784
# vcredist_x64.exe

from pyzbar.pyzbar import decode
from PIL import Image

img = Image.open(sys.argv[2])
print("Image:\n{}\n----------\n".format(img))

result = decode(img)

qrpayload = ""
for i in result:
    qrpayload = qrpayload+i.data.decode("utf-8")
print("QR .. payload:\n{}\n----------\n".format(qrpayload))
payload = qrpayload[4:]

"""
with open(sys.argv[1]) as f:
    lines = f.readlines()
payload = lines[0][4:]
"""
print("decoding payload:\n{}\n----------\n\n".format(payload))

# decode Base45 (remove HC1: prefix)
decoded = base45.b45decode(payload)
 
# decompress using zlib
decompressed = zlib.decompress(decoded)
# decode COSE message (no signature verification done)
cose = CoseMessage.decode(decompressed)
# decode the CBOR encoded payload and print as json
print(json.dumps(cbor2.loads(cose.payload), indent=2))


print("\n\nCoseMessage:\n{}\n----------\n\n".format(cose))


qrdecoded = cbor2.loads(decompressed)

pprint.pprint(cbor2.loads(qrdecoded.value[2]))

# decompressed = CoseMessage.encode(cose.payload)
# compressed = zlib.decompress(decompressed)
# encoded = base45.b45encode(compressed)