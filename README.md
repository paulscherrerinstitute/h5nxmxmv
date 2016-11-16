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
