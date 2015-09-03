#!/bin/sh

# Packages the vendor libraries for UI-prototype
#
# Libraries from google_appengine.zip:
LIBS=('apiclient')

#
# Libraries from virtualenv:
VIRTUAL_ENV_LIBS=('django')

#
# Usage
# create_vendor_libs.sh <appengine_path> <virtualenv_site_packages_path>
#
# appengine_path:      Path to unzipped Google AppEngine distribution (.zip download)
# virtualenv_lib_path: Path to the virtualenv site-packages directory containing the libraries
#                      listed above.


APPENGINE_LIB="$1/lib"
VIRTUAL_ENV=$2
CURRENT_DIR=$PWD

for lib in "${LIBS[@]}"
do
    pushd $APPENGINE_LIB/$lib
    zip -x"*.pyc" -r $CURRENT_DIR/$lib.zip $lib
    popd
done

for lib in "${VIRTUAL_ENV_LIBS[@]}"
do
    pushd $VIRTUAL_ENV
    zip -x"*.pyc" -r $CURRENT_DIR/$lib.zip $lib
    popd
done
