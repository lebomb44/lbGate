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
sudo update-rc.d lbGate defaults
```
