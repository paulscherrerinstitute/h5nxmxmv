#!/usr/bin/env python

import os
import h5py
import logging
import argparse

program_help = '''
This script is meant to make it easier to rename an HDF5
file conforming to the NeXus/nxMX application definition:

  http://download.nexusformat.org/sphinx/classes/applications/NXmx.html

This script will:
    1. create a new hard-link (man 2 link) from source -> destination datafile
    2. update the External Link to point to the destination datafile
    3. remove old source datafile hardlink
    4. rename master file to its new filename

This script DOES NOT:

    - handle overwriting files
        => TIP: check your folder thoroughly!!

    - rename across different filesystems
        => TIP: rename locally and copy it afterwards

CAVEAT:
   Your data is precious right? Test this script in
   your *OWN* environment before using it.
'''

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    epilog=program_help)
parser.add_argument('--dry-run', help='dry run; just print what would happen - activates verbose', action='store_true', default=False)
parser.add_argument('--quiet', dest='verbose', help='be quiet', action='store_false', default=True)
parser.add_argument("source", help='filename of original HDF5 master file')
parser.add_argument("dest", help='new filename of renamed master file and data files accordingly')

try:
    args = parser.parse_args()
except:
    parser.print_help()
    exit(0)

loglvl = logging.WARN
if args.verbose or args.dry_run:
    loglvl = logging.DEBUG

logging.basicConfig(level=loglvl,
    format= '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y.%m.%d %H:%M:%S')

src = args.source
destination = args.dest

# find out destination folder and whether it is writable
#
dst_folder, dst = os.path.split(destination)
if not dst_folder:
    dst_folder = './'
logging.debug('dest folder && file: {} && {}'.format(dst_folder, dst))
if not os.access(dst_folder, os.W_OK):
    logging.fatal('destination folder "{}" is not writable by current user "{}"'.format(
        dst_folder,
        os.getenv('USER')
    ))

src_prefix = src.replace('_master.h5', '')
dst_prefix = dst.replace('_master.h5', '')

if not os.path.exists(src):
    logging.fatal('source master HDF5 file not found: {}'.format(src))
    exit(1)

if not dst.endswith('_master.h5'):
    logging.fatal('dest filename must end with "_master.h5"')
    exit(1)

if os.path.exists(dst):
    logging.fatal('destination {} already exists!'.format(dst))
    logging.fatal('fix this and try again')
    exit(1)

# same filesystem?
logging.debug('filesystem identifier (st_dev) src={} & dst={}'.format(os.stat(src).st_dev, os.stat(dst_folder).st_dev))
same_filesystem = os.stat(src).st_dev == os.stat(dst_folder).st_dev
if not same_filesystem:
    logging.fatal('renaming across filesystems is not supported!')
    logging.error('    =>>> rename in-place then copy renamed dataset')
    exit(1)


if args.dry_run:
    mode = 'r'
else:
    mode = 'a'
logging.info('opening master file in {} mode'.format('read-only' if mode=='r' else 'write'))
h5 = h5py.File(src, mode=mode)


data_keys = []
for k, v in h5['/entry/data'].items():
    data_keys.append(k)
data_keys.sort()

# Build a list of things to rename
#
rename_list = []
for k in data_keys:
    # Get the filename and not the full path to the linked hdf5 file
    h5link = h5['/entry/data'].get(k, getlink=True)
    # it could be HardLink or SoftLink
    if not isinstance(h5link, h5py.ExternalLink):
        logging.fatal('Link "/entry/data/{}" is not an ExternalLink! Aborting...'.format(k))
    srcd = h5link.filename

    if not os.path.exists(srcd):
        logging.error('missing data file: {}'.format(srcd))
        logging.fatal('aborting...')
        exit(1)

    # FIXME following line assumes "srcd" does not
    #       contain a folder specification
    dstd = srcd.replace(src_prefix, dst_prefix, 1)
    dstd = os.path.join(dst_folder, dstd)

    if os.path.exists(dstd):
        logging.fatal('data file already exists: {}'.format(dstd))
        logging.fatal('master file was not there though... bug?!? aborting...')
        logging.fatal('check folder thoroughly and try again')
        exit(1)

    # all good append file
    logging.info('appending {} to rename list'.format((k, srcd, dstd) ))
    rename_list.append( (k, srcd, dstd) )

rename_list.sort()

for k, s, d in rename_list:
    data_key = '/entry/data/{}'.format(k)
    dst_folder, dst = os.path.split(d)
    if args.dry_run:
        logging.info('would rename {} -> {}'.format(s, d))
        logging.info('would modify hdf5 master link \"/entry/data/{}\" => {}'.format(k, dst))
        continue

    logging.info('linking {} -> {}'.format(s, d))
    os.link(s, d)
    logging.info('updating hdf5 key {} -> {}'.format(data_key, dst))
    del h5[data_key]
    h5[data_key] = h5py.ExternalLink(dst, '/entry/data/data')
    logging.info('unlinking {}'.format(s))
    os.unlink(s)

h5.close()

if args.dry_run:
    logging.info('would rename master {} => {}'.format(src, destination))
else:
    os.rename(src, destination)
