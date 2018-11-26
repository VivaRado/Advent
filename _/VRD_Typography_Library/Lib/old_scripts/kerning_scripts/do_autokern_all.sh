#!/bin/bash
BASEDIR=$(dirname "$0")
echo "$BASEDIR"
#
PIDDIR=$BASEDIR/autokern_dir/do_autokern.py
#
python $PIDDIR "$@"