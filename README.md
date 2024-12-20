# Static IP

```shell
sudo vi /etc/dhcpcd.conf
# Example static IP configuration:
interface eth0
static ip_address=192.168.10.4/24
#static ip6_address=fd51:42f8:caae:d92e::ff/64
static routers=192.168.10.1
static domain_name_servers=8.8.8.8
```

# Disable Wifi

```shell
vi /boot/config.txt
dtoverlay=disable-wifi
```

# Get sources

```shell
cd
mkdir workspace
cd workspace
git clone https://github.com/lebomb44/lbGate.git
```
Configure
```shell
cd workspace/lbGate
cp myconfig_example.py myconfig.py
vi myconfig.py
```

# Mount HDD

## Create mount point

```shell
sudo mkdir /media/HDD
```

## /etc/fstab

```shell
/dev/sda1 /media/HDD ext4 nofail 0 0
```

## Create symbol link

```shell
cd
ln -s /media/HDD HDD
```

# Crontab

```shell
0 2 * * * /usr/bin/rsync -a /var/www/html/backup/ /media/HDD/jeedom/backup/
#0 * * * * /home/pi/workspace/lbGate/nginx/check-services.sh > /tmp/check-services.log
0 2 * * * /usr/bin/sudo /usr/bin/certbot renew --quiet
*/5 * * * * /home/pi/workspace/lbGate/vpn/up.sh
```

# Change Jeedom port

```shell
sudo nano /etc/apache2/ports.conf

Listen 8080

<IfModule ssl_module>
        Listen 444
</IfModule>

<IfModule mod_gnutls.c>
        Listen 444
</IfModule>
```

# Install Transmission

## Installation
```shell
sudo apt-get install transmission-daemon
sudo rm /etc/init.d/transmission-daemon
sudo systemctl disable transmission-daemon
Removed symlink /etc/systemd/system/multi-user.target.wants/transmission-daemon.service.
sudo systemctl stop transmission-daemon
```

## Configuration

```shell
sudo nano /home/torrent/.config/transmission-daemon/settings.json
    "download-dir": "/media/HDD/Movies",
    "incomplete-dir": "/media/HDD/Movies",
    "rpc-whitelist-enabled": false,
```


# Install Shell In a Box

```shell
sudo apt-get install shellinabox
```

## Edit Configuration File

```shell
sudo vi /etc/default/shellinabox
SHELLINABOX_ARGS="--no-beep -t"
```

# Create torrent user and change password

```shell
sudo useradd -m torrent
sudo passwd torrent
sudo usermod -a -G video torrent
```

# Nginx

Install Nginx
```shell
sudo apt-get install nginx nginx-extras fcgiwrap php-fpm
```
Configure Nginx
```shell
sudo cp workspace/lbGate/nginx/default /etc/nginx/sites-available/.
sudo cp workspace/lbGate/nginx/nginx.conf /etc/nginx/.
sudo cp -R workspace/lbGate/nginx/html /etc/nginx/.
sudo cp -R workspace/lbGate/nginx/scripts /etc/nginx/.
```
Create users
```shell
cd /etc/nginx/
sudo htpasswd -c .htpasswd user1
sudo htpasswd .htpasswd user2
```

# HTTPS certificate from Let's Encrypt

```shell
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx
```

# tinyfilemanager

Installation
```shell
cd workspace
git clone https://github.com/prasathmani/tinyfilemanager.git
```
Configuration
```shell
vi tinyfilemanager/tinyfilemanager.php
$use_auth = false;
```

# OpenVPN client

```shell
sudo apt install openvpn
sudo cp workspace/lbGate/vpn/client.conf /etc/openvpn/.
sudo cp pass.txt /etc/openvpn/.
sudo cp ca.rsa.4096.crt /etc/openvpn/.
sudo cp crl.rsa.4096.pem /etc/openvpn/.
sudo systemctl enable openvpn@client.service
sudo service openvpn@client start
```

# Set DNS in VPN namespace

```shell
sudo mkdir /etc/netns
sudo mkdir /etc/netns/vpn
sudo vi /etc/netns/vpn/resolv.conf
nameserver 208.67.222.222
nameserver 208.67.220.220-
```

# Torrent namespace

```shell
*/5 * * * * /home/pi/workspace/lbGate/vpn/up.sh
```

# Check VPN namepace IP

```shell
/usr/bin/sudo /bin/ip netns exec vpn curl ifconfig.co
```

# Firewall to forbid VPN namespace access to default namespace (increase security)

## Installation

```shell
sudo apt-get install ufw

sudo ufw default allow outgoing
Default outgoing policy changed to 'allow'
(be sure to update your rules accordingly)

sudo ufw default allow incoming
Default incoming policy changed to 'allow'
(be sure to update your rules accordingly)

sudo ufw reset
Resetting all rules to installed defaults. This may disrupt existing ssh
connections. Proceed with operation (y|n)? y

sudo ufw deny in on vpn0
Rules updated
Rules updated (v6)

sudo ufw enable
Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
Firewall is active and enabled on system startup

sudo ufw status verbose
Status: active
Logging: on (low)
Default: allow (incoming), allow (outgoing)
New profiles: skip

To                         Action      From
--                         ------      ----
Anywhere on vpn0           DENY IN     Anywhere
Anywhere (v6) on vpn0      DENY IN     Anywhere (v6)
```

## Test the firewall protection. The following command must be blocked

```shell
/usr/bin/sudo /bin/ip netns exec vpn ssh osmc@192.168.100.1
```

# Wireguard server

https://www.sigmdel.ca/michel/ha/wireguard/wireguard_02_fr.html
https://wireguard.how/client/raspberry-pi-os/

# lbGate

Create symbolic link to serial port
```shell
sudo apt-get install usbutils
sudo nano /etc/udev/rules.d/98-usb-serial.rules
SUBSYSTEM=="tty", ATTRS{idVendor}=="0658", ATTRS{idProduct}=="0200", SYMLINK+="ttyUSB21"
SUBSYSTEM=="tty", ATTRS{product}=="RFPLAYER", SYMLINK+="rfplayer", RUN+="/bin/stty -F /dev/rfplayer -parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts -ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr -icrnl -ixon -ixoff -iuclc -ixany -imaxbel iutf8 -opost -olcuc -ocrnl -onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig -icanon iexten -echo -echoe -echok -echonl noflsh -xcase -tostop -echoprt -echoctl -echoke min 0 time 0 speed 115200"
SUBSYSTEM=="tty", ATTRS{devpath}=="1.5.3"  , SYMLINK+="safety" , RUN+="/bin/stty -F /dev/safety  -parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts -ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr -icrnl -ixon -ixoff -iuclc -ixany -imaxbel iutf8 -opost -olcuc -ocrnl -onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig -icanon iexten -echo -echoe -echok -echonl noflsh -xcase -tostop -echoprt -echoctl -echoke min 0 time 0 speed 115200" 
SUBSYSTEM=="tty", ATTRS{devpath}=="1.5.2"  , SYMLINK+="dining" , RUN+="/bin/stty -F /dev/dining  -parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts -ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr -icrnl -ixon -ixoff -iuclc -ixany -imaxbel iutf8 -opost -olcuc -ocrnl -onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig -icanon iexten -echo -echoe -echok -echonl noflsh -xcase -tostop -echoprt -echoctl -echoke min 0 time 0 speed 115200"
SUBSYSTEM=="tty", ATTRS{devpath}=="1.5.1"  , SYMLINK+="kitchen", RUN+="/bin/stty -F /dev/kitchen -parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts -ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr -icrnl -ixon -ixoff -iuclc -ixany -imaxbel iutf8 -opost -olcuc -ocrnl -onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig -icanon iexten -echo -echoe -echok -echonl noflsh -xcase -tostop -echoprt -echoctl -echoke min 0 time 0 speed 115200"
SUBSYSTEM=="tty", ATTRS{devpath}=="1.5.4.3", SYMLINK+="bedroom", RUN+="/bin/stty -F /dev/bedroom -parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts -ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr -icrnl -ixon -ixoff -iuclc -ixany -imaxbel iutf8 -opost -olcuc -ocrnl -onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig -icanon iexten -echo -echoe -echok -echonl noflsh -xcase -tostop -echoprt -echoctl -echoke min 0 time 0 speed 115200"
SUBSYSTEM=="tty", ATTRS{devpath}=="1.5.4.2", SYMLINK+="ext"    , RUN+="/bin/stty -F /dev/ext     -parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts -ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr -icrnl -ixon -ixoff -iuclc -ixany -imaxbel iutf8 -opost -olcuc -ocrnl -onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig -icanon iexten -echo -echoe -echok -echonl noflsh -xcase -tostop -echoprt -echoctl -echoke min 0 time 0 speed 115200"
SUBSYSTEM=="tty", ATTRS{devpath}=="1.5.4.1", SYMLINK+="entry"  , RUN+="/bin/stty -F /dev/entry   -parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts -ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr -icrnl -ixon -ixoff -iuclc -ixany -imaxbel iutf8 -opost -olcuc -ocrnl -onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig -icanon iexten -echo -echoe -echok -echonl noflsh -xcase -tostop -echoprt -echoctl -echoke min 0 time 0 speed 115200"
SUBSYSTEM=="tty", ATTRS{devpath}=="1.5.4.4.3", SYMLINK+="heatpump", RUN+="/bin/stty -F /dev/heatpump -parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts -ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr -icrnl -ixon -ixoff -iuclc -ixany -imaxbel iutf8 -opost -olcuc -ocrnl -onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig -icanon iexten -echo -echoe -echok -echonl noflsh -xcase -tostop -echoprt -echoctl -echoke min 0 time 0 speed 115200" 
SUBSYSTEM=="tty", ATTRS{devpath}=="1.5.4.4.4", SYMLINK+="sms"  , RUN+="/bin/stty -F /dev/sms     -parenb -parodd -cmspar cs8 hupcl -cstopb cread clocal -crtscts -ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr -icrnl -ixon -ixoff -iuclc -ixany -imaxbel -iutf8 -opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig -icanon -iexten -echo -echoe -echok -echonl -noflsh -xcase -tostop -echoprt -echoctl -echoke -flusho -extproc min 0 time 0 speed 115200"

```
Enable lbGate service
```shell
sudo cp workspace/lbGate/service/lbGate /etc/init.d/.
sudo update-rc.d lbGate defaults
```

# Public account

Create pulic user account
```shell
sudo useradd -m public
sudo passwd public
sudo chown root:root /home/public
sudo chmod 755 /home/public
```
Limit usage to SFTP only
```shell
sudo vi /etc/ssh/sshd_config
#Subsystem sftp /usr/lib/openssh/sftp-server
Subsystem sftp internal-sftp

Match User public
    ChrootDirectory %h
    ForceCommand internal-sftp
    AllowTCPForwarding no
    X11Forwarding no
```
Create mounting points
```shell
sudo mkdir /home/public/Movies
sudo mkdir /home/public/Music
```
Mount folders at startup
```shell
sudo vi /etc/fstab
/media/HDD/Movies /home/public/Movies none nofail,x-systemd.device-timeout=9,bind,ro
/media/HDD/Music /home/public/Music none nofail,x-systemd.device-timeout=9,bind,ro
```

Samba
```shell
sudo apt-get install samba samba-common-bin
sudo nano /etc/samba/smb.conf
####### Authentication #######
   server role = standalone server
   security = user

#======================= Share Definitions =======================
;[printers]
;   comment = All Printers
;   browseable = no
;   path = /var/spool/samba
;   printable = yes
;   guest ok = no
;   read only = yes
;   create mask = 0700
;[print$]
;   comment = Printer Drivers
;   path = /var/lib/samba/printers
;   browseable = yes
;   read only = yes
;   guest ok = no
[public]
  comment= Public Storage
  path = /home/public/Movies
  guest ok = yes
  guest only = yes
  writable = no
  force create mode = 0666
  force directory mode = 0777
  browseable = yes
sudo /etc/init.d/smbd restart
```
