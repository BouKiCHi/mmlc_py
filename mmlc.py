#!/bin/env python3


import sys
import os
from mml_module.driver import Driver

from mml_module.mmlfile import MMLFile
from mml_module.output import Output

argc = len(sys.argv)
if argc < 2:
    print("Usage mmlc.py <mmlfile>")
    exit()

infile = sys.argv[1]
print("file:%s" % infile)
if not os.path.exists(infile):
    print("File not found!")
    exit()


inst = MMLFile(infile)
if not inst.compile():
    exit()

out = Output("output.mid")
driver = Driver(inst.data, out)
driver.drive()
out.write()

