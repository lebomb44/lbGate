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

sudo useradd -m torrent
sudo passwd torrent
