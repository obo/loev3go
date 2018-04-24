#!/bin/bash
# run this once to populate a new robot home directory

function warn() { echo "$@" >&2; }
function die() { echo "$@" >&2; exit 1; }
set -o pipefail  # safer pipes
set -e # die on any error

MYDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" # get script directory

if [ -e $HOME/.vimrc ]; then
  warn "~/.vimrc exists, not touching"
else
  ln -s $MYDIR/vimrc $HOME/.vimrc || die "Failed to symlink .vimrc"
fi

if [ -e $HOME/.bashrc ]; then
  warn "~/.bashrc exists, not touching"
else
  ln -s $MYDIR/bashrc $HOME/.bashrc || die "Failed to symlink .bashrc"
fi
