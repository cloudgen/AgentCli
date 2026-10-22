#!/bin/sh
# Python ship unit. The POSIX reference suite remains tests/run.sh.
set -eu
root=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
cd "$root"
export PYTHONPATH="${root}/src${PYTHONPATH:+:$PYTHONPATH}"
exec python3 -m unittest discover -s tests "$@"
