#!/bin/bash

ifnstun0=`/usr/bin/sudo /bin/ip netns exec vpn /sbin/ifconfig tun0`
errnoifnstun0=$?

tdpid=`/usr/bin/sudo /bin/pidof transmission-daemon`
errnotdpid=$?

if [ $errnoifnstun0 -eq 0 -a $errnotdpid -eq 0 ]; then
	echo "TUN0 already in vpn namespace"
	echo "Transmission Daemon already running"
	exit 1
fi

if [ $errnoifnstun0 -ne 0 ]; then
	echo "#############################################"
	echo "### Remove all default routes in VPN namespace if any ###"
	/usr/bin/sudo /bin/ip netns exec vpn /bin/ip route flush 0/0
	/usr/bin/sudo /bin/ip netns

	echo "##############################"
	echo "### Creating VPN namespace ###"
	/usr/bin/sudo /bin/ip netns add vpn
	sleep 1
	/usr/bin/sudo /bin/ip netns exec vpn /bin/ip link list
	/usr/bin/sudo /bin/ip netns exec vpn /bin/ip link set dev lo up

	echo "###########################"
	echo "### Creating inter link ###"
	/usr/bin/sudo /bin/ip link add vpn0 type veth peer name vpn1
	sleep 1
	/usr/bin/sudo /bin/ip link set vpn1 netns vpn
	sleep 1
	/usr/bin/sudo /bin/ip netns exec vpn /bin/ip link list

	echo "##############################"
	echo "### Setting inter link IPs ###"
	/usr/bin/sudo /bin/ip netns exec vpn /sbin/ifconfig vpn1 192.168.100.2/24 up
	/usr/bin/sudo /bin/ip netns exec vpn /sbin/ifconfig vpn1
	/usr/bin/sudo /sbin/ifconfig vpn0 192.168.100.1/24 up
	/usr/bin/sudo /bin/ip netns exec vpn /sbin/route -n

	iftun0=`/usr/bin/sudo /sbin/ifconfig tun0`
	if [ $? -eq 0 ]; then
		echo "####################################"
		echo "### Get data from tun0 interface ###"
		TUN0_ADDR=`/usr/bin/sudo /sbin/ifconfig tun0 | grep -oP 'inet \K\S+'`
		TUN0_PTP=`/usr/bin/sudo /sbin/ifconfig tun0 | grep -oP 'destination \K\S+'`
		TUN0_MASK=`/usr/bin/sudo /sbin/ifconfig tun0 | grep -oP 'netmask \K\S+'`
		echo "TUN0 ADDR = $TUN0_ADDR"
		echo "TUN0 PTP = $TUN0_PTP"
		echo "TUN0 MASK = $TUN0_MASK"

		echo "#########################################"
		echo "### Transfering TUN0 to VPN namespace ###"
		/usr/bin/sudo /bin/ip link set tun0 netns vpn
		echo "#################################"
		echo "###Configuring TUN0 interface ###"
		/usr/bin/sudo /bin/ip netns exec vpn /sbin/ifconfig tun0 inet $TUN0_ADDR netmask $TUN0_MASK dstaddr $TUN0_PTP up
		echo "###############################################"
		echo "### Adding default gateway in VPN namespace ###"
		/usr/bin/sudo /bin/ip netns exec vpn /sbin/route add default gw $TUN0_PTP
	fi
	echo "############################################"
	echo "### Show the result of the configuration ###"
	/usr/bin/sudo /bin/ip netns exec vpn /sbin/ifconfig
	/usr/bin/sudo /bin/ip netns exec vpn /sbin/route -n
fi

if [ $errnoifnstun0 -ne 0 -o $errnotdpid -ne 0 ]; then
	echo "#################################"
	echo "### Remove old process if any ###"
	if [ "$tdpid" != "" ]; then
		/usr/bin/sudo /bin/kill $tdpid
		echo "Process $tdpid killed"
		/bin/sleep 10
	fi
	echo "############################"
	echo "### Launch server ###"
	#/usr/bin/sudo /bin/ip netns exec vpn /usr/bin/sudo /bin/su torrent -c "/usr/bin/python /usr/bin/deluged -d -c /home/deluge/config -l /home/deluge/deluged.log -L info &"
	#/usr/bin/sudo /bin/ip netns exec vpn /usr/bin/sudo /bin/su torrent -c "/usr/bin/python /usr/bin/deluge-web -c /home/deluge/config -l /home/deluge/deluge-web.log -L info &"
	/usr/bin/sudo /bin/ip netns exec vpn /usr/bin/sudo /bin/su torrent -c "/usr/bin/transmission-daemon -f --log-error --log-info --log-debug -g /home/torrent/.config/transmission-daemon &"
fi

