#!/bin/bash

set -e
set -x

if [ -z ${VIRTUAL_ENV+x} ]; then
	echo "It is recommended that you run this while in a Virtual Environment";
	exit 1;
fi

pip install -r requirements.txt
