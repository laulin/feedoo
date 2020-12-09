echo "dnsmasq : "
wc -l tests/input/dnsmasq*.log
wc -l tests/output/jarvis-2/dnsmasq*
echo "health : "
wc -l tests/input/health*.log
wc -l tests/output/jarvis-2/health*
echo "netflow : "
wc -l tests/input/netflow*.log
wc -l tests/output/jarvis-2/netflow*
echo "sys : "
wc -l tests/input/sys*.log
wc -l tests/output/jarvis-2/sys*
echo "log : "
wc -l tests/input/log*.log
wc -l tests/output/jarvis-2/log*