#!/bin/bash

function die() { echo "$@" >&2; exit 1; }
set -o pipefail  # safer pipes

[ ! -z "$1" ] || die "usage: $0 <ip-as-shown-on-robot>"
robotip="$1"

robotintf=$(ifconfig | grep "HWaddr 12:16" | cut -d" " -f1)
if [ -z "$robotintf" ]; then
  die "Robot does not seem connected!"
fi

myip=$(echo $robotip | cut -d. -f1-3).1
echo "Robot seems connected at the interface: $robotintf"
echo "Now enter your password for sudo, if needed."
sudo ifconfig $robotintf $myip \
|| die "Failed to set our IP"

echo "# To connect to robot, use:"
echo "  source ensure_ssh_agent  # Ondrej's trick to reuse/run ssh-agent"
echo "  ssh-add $(first_existing ~/.ssh/id_rsa_for_ev3)"
echo "  ssh robot@$robotip"
echo "# And on robot to get routing to Internet:"
echo "  sudo /sbin/route add default gw $myip"
echo '  echo "nameserver 1.1.1.1" | sudo tee /etc/resolv.conf'

