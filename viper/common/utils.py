# This file is part of Viper - https://github.com/viper-framework/viper
# See the file 'LICENSE' for copying permission.

import os
import sys
import string
import hashlib

try:
    import magic
except ImportError:
    pass

# Taken from the Python Cookbook.
def path_split_all(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path:
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])

    return allparts

# The following couple of functions are redundant.
# TODO: find a way to better integrate these generic methods
# with the ones available in the File class.
def get_type(data):
    try:
        ms = magic.open(magic.MAGIC_NONE)
        ms.load()
        file_type = ms.buffer(data)
    except:
        try:
            file_type = magic.from_buffer(data)
        except:
            return ''
    finally:
        try:
            ms.close()
        except:
            pass

    return file_type

def get_md5(data):
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()

def string_clean(line):
    try:
        return filter(lambda x: x in string.printable, line)
    except:
        return line

# Snippet taken from:
# https://gist.github.com/sbz/1080258
def hexdump(src, length=16, maxlines=None):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))

        if maxlines:
            if len(lines) == maxlines:
                break

    return ''.join(lines)
