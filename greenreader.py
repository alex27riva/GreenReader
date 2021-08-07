#!/usr/bin/env python3

import zlib
import base45
import cbor2
import pprint
import argparse
import PIL.Image
import pyzbar.pyzbar

parser = argparse.ArgumentParser(description='Decode Green Pass QR code')
parser.add_argument('--image', help='path to QR code image')

args = parser.parse_args()

# exit if no image provided
if args.image is None:
    print('No image provided')
    exit()

# read QR code from image
data = pyzbar.pyzbar.decode(PIL.Image.open(args.image))
cert = data[0].data.decode()

# remove 'HC1:'
b45data = cert.replace("HC1:", "")

# decode base45 string
zlib_data = base45.b45decode(b45data)

# decompress zlib compressed data
decompressed_data = zlib.decompress(zlib_data)

# decode cbor object
decoded = cbor2.loads(decompressed_data)

# print data
pprint.pprint(cbor2.loads(decoded.value[2]))