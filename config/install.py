#!/usr/bin/env python
#
# Script to apply substitutions to a subtree of files.
# Specific for the Atrium-ONOS distribution.
#

import sys
import os
import re
import socket
from collections import OrderedDict

def get_onos_ip_addr():
    """
    Get the local IP address

    Hack from stack overflow.
    """
    full_list = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) \
                 for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]]
    return full_list[0][1]

def gen_subs_list():
    subs_list = OrderedDict()
    onos_ip = get_onos_ip_addr()
    # Truncate IP to get the "candidate IPs" for cell definition
    tmp_ar = onos_ip.split(".")[0:3]
    tmp_ar.append("*")
    onos_subnet_starred = ".".join(tmp_ar)
    # subs_list["foo"] = "bar"
    subs_list["__ONOS_IP_ADDR__"] = onos_ip
    subs_list["__ONOS_SUBNET_STARRED__"] = onos_subnet_starred
    return subs_list
    
def update_content(file_content, subs_list):
    new_content = []
    changed = False
    for line in file_content:
        for k, v in subs_list.items():
            if re.search(k, line):
                changed = True
            line = re.sub(k, v, line)
        new_content.append(line)
    # Could check if changed is True
    return new_content

def process_files(source_root, target_root):
    try:
        os.makedirs(target_root)
    except:
        pass
    subs_list = gen_subs_list()
    for subdir, dirs, files in os.walk(source_root):
        relative_dir = subdir.replace(source_root, "").strip("/")
        target_subdir = os.path.join(target_root, relative_dir)
        try:
            os.makedirs(target_subdir)
        except:
            pass
        for file in files:
            in_filename = os.path.join(subdir, file)
            out_filename = os.path.join(target_subdir, file)
#            print("In: %s" % in_filename)
#            print("  Out: %s" % out_filename)
            with open(in_filename, "r") as f:
                file_content = f.readlines()
            new_content = update_content(file_content, subs_list)
            with open(out_filename, "w") as f:
                f.write("".join(new_content))

if __name__ == "__main__":
    # Source is co-located with this script
    source_root = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "config-root")

    if len(sys.argv) == 2:
        target_root = sys.argv[1]
    else:
        target_root = os.path.expanduser("~")

#    if 'ONOS_IP_ADDR' in os.environ: # Could consider using this
#        pass

#    if len(sys.argv) != 3:
#        print("Error: Specify source and destination directories")
#        exit(1)

    print("Installing Atrium BGP configuration files")
    print("  Source:       %s" % source_root)
    print("  Destination:  %s" % target_root)
    process_files(source_root, target_root)
