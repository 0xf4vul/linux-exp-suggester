#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import shutil
import urllib
import platform
from optparse import OptionParser


h00lyshit = {
    'Name': 'h00lyshit',
    'Kernel': [
        '2.6.8',  '2.6.10', '2.6.11', '2.6.12',
        '2.6.13', '2.6.14', '2.6.15', '2.6.16',
    ],
    'CVE': '2006-3626',
    'Source': 'http://www.exploit-db.com/exploits/2013/',
}
elflbl = {
    'Name': 'elflbl',
    'Kernel': ['2.4.29'],
    'Source': 'http://www.exploit-db.com/exploits/744/',
}
krad3 = {
    'Name': 'krad3',
    'Kernel': ['2.6.5', '2.6.7', '2.6.8', '2.6.9', '2.6.10', '2.6.11'],
    'Source': 'http://exploit-db.com/exploits/1397/',
}
w00t = {
    'Name': 'w00t',
    'Kernel': ['2.4.10', '2.4.16', '2.4.17', '2.4.18', '2.4.19', '2.4.20', '2.4.21'],
    'Source': '',
}
brk = {
    'Name': 'brk',
    'Kernel': ['2.4.10', '2.4.18', '2.4.19', '2.4.20', '2.4.21', '2.4.22'],
    'Source': '',
}
elfdump = {
    'Name': 'elfdump',
    'Kernel': ['2.4.27'],
    'Source': '',
}
elfcd = {
    'Name': 'elfcd',
    'Kernel': ['2.6.12'],
    'Source': '',
}
expand_stack = {
    'Name': 'expand_stack',
    'Kernel': ['2.4.29'],
    'Source': '',
}
kdump = {
    'Name': 'kdump',
    'Kernel': ['2.6.13'],
    'Source': '',

}
km2 = {
    'Name': 'km2',
    'Kernel': ['2.4.18', '2.4.22'],
    'Source': '',
}
krad = {
    'Name': 'krad',
    'Kernel': ['2.6.5', '2.6.7', '2.6.8', '2.6.9', '2.6.10', '2.6.11'],
    'Source': '',
}

exploits = [h00lyshit, elflbl, krad, krad3, w00t, elfdump, brk, elfcd, expand_stack, kdump, km2]

def get_exploits(kernel_version, is_partial, is_download):
    prog = re.compile(kernel_version)
    for exploit in exploits:
        if prog.search(str(exploit['Kernel'])):
            print '[+] ' + exploit['Name']
            print_exploit(exploit)
            if is_download:
                url = exploit['Source']
                download_exp(url, exploit['Name'], kernel_version)


def download_exp(url, name, kernel_version):
    if 'exploit-db' in url:
        down_url = url.replace('exploits', 'download')
    else:
        down_url = url
    dir_name = 'exploits_' + kernel_version
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    try:
        urllib.urlretrieve(down_url, name)
        filename = add_suffix(name)
        shutil.move(filename, dir_name)
    except Exception, e:
        print '[-] Download {name} failed'.format(name=name)


def add_suffix(file):
    suffix = file_type(file)
    filename = file + suffix
    shutil.move(file, filename)
    return filename


def file_type(path):
    content = file(path).read()
    if 'stdio.h' in content:
        suffix = '.c'
    elif 'python' in content:
        suffix = '.py'
    elif 'perl' in content:
        suffix = '.pl'
    else:
        suffix = ''
    return suffix


def print_exploit(exploit):
    for _ in exploit:
        if _ != 'Name':
            print '    ' + _ + ':  ' + str(exploit[_])


def get_kernel_version():
    uname = platform.uname()
    system = uname[0]
    if system == 'Linux':
        kernel_version = uname[2]
    else:
        kernel_version = ''
        print '[-] local system is {system}!, please use -k'.format(system=system)
        sys.exit(0)
    return kernel_version


def main():
    parser = OptionParser()
    parser.add_option("-k", "--kernel_version",
                      dest="kernel_version", help="kernel version number eg.2.6.8")
    parser.add_option("--download",
                      action="store_true", dest="is_download", default=False, help="download match exploits")
    (options, args) = parser.parse_args()
    if options.kernel_version:
        kernel_version = options.kernel_version
    else:
        kernel_version = get_kernel_version()
    if re.match('\d+\.\d+\.\d+', kernel_version):
        is_partial = False
    else:
        is_partial = True

    print kernel_version
    print
    get_exploits(kernel_version, is_partial, options.is_download)

if __name__ == "__main__":
    main()
