#!/usr/bin/env bash
IFACE=enx00e04c680253
IP=169.254.49.1/16

echo "Fixing redpitaya network on $IFACE..."

sudo nmcli device set $IFACE managed no 2>/dev/null || true
sleep 1
ip link set $IFACE down
sleep 1
ip addr flush dev $IFACE
sleep 1
ip addr add $IP dev $IFACE
sleep 1
ip link set $IFACE up
sleep 2

echo "Interface configured:"
ip addr show $IFACE | grep inet

echo "Testing connection..."
ping -c 3 169.254.49.194