HDF5 NeXus nxMX File Renaming Utility
======================================

This script is meant to make it easier to rename an HDF5
file conforming to the NeXus/nxMX application definition:

  http://download.nexusformat.org/sphinx/classes/applications/NXmx.html

## This script will:

1. create a new [hard-link](http://man7.org/linux/man-pages/man2/link.2.html) from source -> destination datafile
2. update all of the *External Links* contained in the master file to point to the renamed destination datafile
3. remove old source datafile hardlink from the filesystem
4. rename master file to its new filename

## This script will NOT:

- handle overwriting files - it will refuse to proceed if it
  detects the possibility of overwriting files
    * **TIP** check your folder thoroughly!!
- rename across different filesystems
    * **TIP** rename locally and copy it afterwards

## CAVEAT
* Your data is precious right? **Test this script in your _OWN_ environment before using it.**


# Example

### before renaming
     $ ls -l
    total 4341776
    -rw-r--r-- 1 zac e10003 302602330 Nov 16 17:11 insulin_data_000001.h5
    -rw-r--r-- 1 zac e10003 292568914 Nov 16 17:11 insulin_data_000002.h5
    -rw-r--r-- 1 zac e10003 288004094 Nov 16 17:11 insulin_data_000003.h5
    -rw-r--r-- 1 zac e10003 285617328 Nov 16 17:11 insulin_data_000004.h5
    -rw-r--r-- 1 zac e10003 285703662 Nov 16 17:11 insulin_data_000005.h5
    -rw-r--r-- 1 zac e10003 292002797 Nov 16 17:11 insulin_data_000006.h5
    -rw-r--r-- 1 zac e10003 311196776 Nov 16 17:11 insulin_data_000007.h5
    -rw-r--r-- 1 zac e10003 299265071 Nov 16 17:11 insulin_data_000008.h5
    -rw-r--r-- 1 zac e10003 290697144 Nov 16 17:11 insulin_data_000009.h5
    -rw-r--r-- 1 zac e10003 287289855 Nov 16 17:11 insulin_data_000010.h5
    -rw-r--r-- 1 zac e10003 286723348 Nov 16 17:11 insulin_data_000011.h5
    -rw-r--r-- 1 zac e10003 287216069 Nov 16 17:11 insulin_data_000012.h5
    -rw-r--r-- 1 zac e10003 293292901 Nov 16 17:11 insulin_data_000013.h5
    -rw-r--r-- 1 zac e10003 312834052 Nov 16 17:11 insulin_data_000014.h5
    -rw-r--r-- 1 zac e10003 125188025 Nov 16 17:11 insulin_data_000015.h5
    -rw-r--r-- 1 zac e10003 205730557 Nov 16 17:12 insulin_master.h5

### during renaming
     $ /exchange/mx/daplus/git/h5nxmxmv/h5nxmxmv.py insulin_master.h5 lysozyme_master.h5
    DEBUG - dest folder && file: ./ && lysozyme_master.h5
    DEBUG - filesystem identifier (st_dev) src=64512 & dst=64512
    INFO - opening master file in write mode
    INFO - creating task list
    INFO - ...add task data_000001: insulin_data_000001.h5 => ./lysozyme_data_000001.h5
    INFO - ...add task data_000002: insulin_data_000002.h5 => ./lysozyme_data_000002.h5
    INFO - ...add task data_000003: insulin_data_000003.h5 => ./lysozyme_data_000003.h5
    INFO - ...add task data_000004: insulin_data_000004.h5 => ./lysozyme_data_000004.h5
    INFO - ...add task data_000005: insulin_data_000005.h5 => ./lysozyme_data_000005.h5
    INFO - ...add task data_000006: insulin_data_000006.h5 => ./lysozyme_data_000006.h5
    INFO - ...add task data_000007: insulin_data_000007.h5 => ./lysozyme_data_000007.h5
    INFO - ...add task data_000008: insulin_data_000008.h5 => ./lysozyme_data_000008.h5
    INFO - ...add task data_000009: insulin_data_000009.h5 => ./lysozyme_data_000009.h5
    INFO - ...add task data_000010: insulin_data_000010.h5 => ./lysozyme_data_000010.h5
    INFO - ...add task data_000011: insulin_data_000011.h5 => ./lysozyme_data_000011.h5
    INFO - ...add task data_000012: insulin_data_000012.h5 => ./lysozyme_data_000012.h5
    INFO - ...add task data_000013: insulin_data_000013.h5 => ./lysozyme_data_000013.h5
    INFO - ...add task data_000014: insulin_data_000014.h5 => ./lysozyme_data_000014.h5
    INFO - ...add task data_000015: insulin_data_000015.h5 => ./lysozyme_data_000015.h5
    INFO - executing task list
    INFO - ...linking insulin_data_000001.h5 -> ./lysozyme_data_000001.h5
    INFO - .....updating hdf5 key /entry/data/data_000001 -> lysozyme_data_000001.h5
    INFO - .....unlinking insulin_data_000001.h5
    INFO - ...linking insulin_data_000002.h5 -> ./lysozyme_data_000002.h5
    INFO - .....updating hdf5 key /entry/data/data_000002 -> lysozyme_data_000002.h5
    INFO - .....unlinking insulin_data_000002.h5
    INFO - ...linking insulin_data_000003.h5 -> ./lysozyme_data_000003.h5
    INFO - .....updating hdf5 key /entry/data/data_000003 -> lysozyme_data_000003.h5
    INFO - .....unlinking insulin_data_000003.h5
    INFO - ...linking insulin_data_000004.h5 -> ./lysozyme_data_000004.h5
    INFO - .....updating hdf5 key /entry/data/data_000004 -> lysozyme_data_000004.h5
    INFO - .....unlinking insulin_data_000004.h5
    INFO - ...linking insulin_data_000005.h5 -> ./lysozyme_data_000005.h5
    INFO - .....updating hdf5 key /entry/data/data_000005 -> lysozyme_data_000005.h5
    INFO - .....unlinking insulin_data_000005.h5
    INFO - ...linking insulin_data_000006.h5 -> ./lysozyme_data_000006.h5
    INFO - .....updating hdf5 key /entry/data/data_000006 -> lysozyme_data_000006.h5
    INFO - .....unlinking insulin_data_000006.h5
    INFO - ...linking insulin_data_000007.h5 -> ./lysozyme_data_000007.h5
    INFO - .....updating hdf5 key /entry/data/data_000007 -> lysozyme_data_000007.h5
    INFO - .....unlinking insulin_data_000007.h5
    INFO - ...linking insulin_data_000008.h5 -> ./lysozyme_data_000008.h5
    INFO - .....updating hdf5 key /entry/data/data_000008 -> lysozyme_data_000008.h5
    INFO - .....unlinking insulin_data_000008.h5
    INFO - ...linking insulin_data_000009.h5 -> ./lysozyme_data_000009.h5
    INFO - .....updating hdf5 key /entry/data/data_000009 -> lysozyme_data_000009.h5
    INFO - .....unlinking insulin_data_000009.h5
    INFO - ...linking insulin_data_000010.h5 -> ./lysozyme_data_000010.h5
    INFO - .....updating hdf5 key /entry/data/data_000010 -> lysozyme_data_000010.h5
    INFO - .....unlinking insulin_data_000010.h5
    INFO - ...linking insulin_data_000011.h5 -> ./lysozyme_data_000011.h5
    INFO - .....updating hdf5 key /entry/data/data_000011 -> lysozyme_data_000011.h5
    INFO - .....unlinking insulin_data_000011.h5
    INFO - ...linking insulin_data_000012.h5 -> ./lysozyme_data_000012.h5
    INFO - .....updating hdf5 key /entry/data/data_000012 -> lysozyme_data_000012.h5
    INFO - .....unlinking insulin_data_000012.h5
    INFO - ...linking insulin_data_000013.h5 -> ./lysozyme_data_000013.h5
    INFO - .....updating hdf5 key /entry/data/data_000013 -> lysozyme_data_000013.h5
    INFO - .....unlinking insulin_data_000013.h5
    INFO - ...linking insulin_data_000014.h5 -> ./lysozyme_data_000014.h5
    INFO - .....updating hdf5 key /entry/data/data_000014 -> lysozyme_data_000014.h5
    INFO - .....unlinking insulin_data_000014.h5
    INFO - ...linking insulin_data_000015.h5 -> ./lysozyme_data_000015.h5
    INFO - .....updating hdf5 key /entry/data/data_000015 -> lysozyme_data_000015.h5
    INFO - .....unlinking insulin_data_000015.h5
    INFO - execution finished
    INFO - closing master hdf5 file
    INFO - renaming master hdf5 file insulin_master.h5 => lysozyme_master.h5
    INFO - finished.

### after renaming
     $ ls -l
    total 4341776
    -rw-r--r-- 1 zac e10003 302602330 Nov 16 17:11 lysozyme_data_000001.h5
    -rw-r--r-- 1 zac e10003 292568914 Nov 16 17:11 lysozyme_data_000002.h5
    -rw-r--r-- 1 zac e10003 288004094 Nov 16 17:11 lysozyme_data_000003.h5
    -rw-r--r-- 1 zac e10003 285617328 Nov 16 17:11 lysozyme_data_000004.h5
    -rw-r--r-- 1 zac e10003 285703662 Nov 16 17:11 lysozyme_data_000005.h5
    -rw-r--r-- 1 zac e10003 292002797 Nov 16 17:11 lysozyme_data_000006.h5
    -rw-r--r-- 1 zac e10003 311196776 Nov 16 17:11 lysozyme_data_000007.h5
    -rw-r--r-- 1 zac e10003 299265071 Nov 16 17:11 lysozyme_data_000008.h5
    -rw-r--r-- 1 zac e10003 290697144 Nov 16 17:11 lysozyme_data_000009.h5
    -rw-r--r-- 1 zac e10003 287289855 Nov 16 17:11 lysozyme_data_000010.h5
    -rw-r--r-- 1 zac e10003 286723348 Nov 16 17:11 lysozyme_data_000011.h5
    -rw-r--r-- 1 zac e10003 287216069 Nov 16 17:11 lysozyme_data_000012.h5
    -rw-r--r-- 1 zac e10003 293292901 Nov 16 17:11 lysozyme_data_000013.h5
    -rw-r--r-- 1 zac e10003 312834052 Nov 16 17:11 lysozyme_data_000014.h5
    -rw-r--r-- 1 zac e10003 125188025 Nov 16 17:11 lysozyme_data_000015.h5
    -rw-r--r-- 1 zac e10003 205730556 Nov 16 17:14 lysozyme_master.h5
