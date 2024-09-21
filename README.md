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
