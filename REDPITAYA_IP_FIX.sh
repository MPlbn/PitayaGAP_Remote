IFACE = "enx00e04c680253"
IP = "169.254.49.1/16"

echo "Fixing redpitaya network on $IFACE..."

sudo ip link set "$IFACE" down
sudo ip addr flush dev "$IFACE"
sudo ip addr add "$IP" dev "$IFACE"
sudo ip link set "$IFACE" up

echo "Interface configured:"
ip addr show "$IFACE" | grep inet

echo "Testing connection..."
ping -c 3 169.254.49.194