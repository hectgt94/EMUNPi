#!/usr/bin/env python
import subprocess

try: 
    subprocess.check_output(['./YT_stream.sh'])
except subprocess.CalledProcessError as e:
    print e.output
