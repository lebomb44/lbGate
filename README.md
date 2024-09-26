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

```shell
sudo apt-get install transmission-daemon
sudo rm /etc/init.d/transmission-daemon
sudo systemctl disable transmission-daemon
Removed symlink /etc/systemd/system/multi-user.target.wants/transmission-daemon.service.
sudo systemctl stop transmission-daemon
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

# Wireguard client

# Torrent namespace

# Wireguard server

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
