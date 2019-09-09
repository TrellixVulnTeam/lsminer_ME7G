#!/bin/bash
sync

echo ""
echo "Mr.Miner is being configured"
echo ---------------------------
echo ""
echo "Files copying..."
echo ""
rsync -aqr --no-perms --no-owner --no-group /root/mrminer/etc/screenrc.mrminer /home/mrminer/screenrc.mrminer
rsync -aqr --no-perms --no-owner --no-group /root/mrminer/etc/screenrc.console /home/mrminer/screenrc.console
rsync -aqr --no-perms --no-owner --no-group /root/mrminer/etc/MinerScreen.desktop /home/mrminer/.config/autostart/MinerScreen.desktop
rsync -aqr --no-perms --no-owner --no-group /root/mrminer/etc/wallpaper.jpg /home/mrminer/wallpaper.jpg
rsync -aqr --no-perms --no-owner --no-group /root/mrminer/etc/xorg.conf.amd /home/mrminer/xorg.conf.amd
rsync -aqr --no-perms --no-owner --no-group /root/mrminer/etc/grub /etc/default/grub
rsync -aqr --no-perms --no-owner --no-group /root/mrminer/etc/crontab /etc/crontab
rsync -aqr --no-perms --no-owner --no-group /root/mrminer/etc/teleconsole /usr/local/bin
rsync -aqr --no-perms --no-owner --no-group /root/mrminer/etc/Prepare.service /etc/systemd/system/Prepare.service
rsync -aqr --no-perms --no-owner --no-group /root/mrminer/etc/Miner.service /etc/systemd/system/Miner.service
rsync -aqr --no-perms --no-owner --no-group /root/mrminer/etc/Sync.service /etc/systemd/system/Sync.service
rsync -aqr --no-perms --no-owner --no-group /root/mrminer/etc/Screen.service /etc/systemd/system/Screen.service
sync

echo "Activating services..."
echo ""
[ ! -f /etc/systemd/system/Prepare.service ] && echo "Service loaded: Prepare" && systemctl enable Prepare
[ ! -f /etc/systemd/system/Miner.service ] && echo "Service loaded: Miner" && systemctl enable Miner
[ ! -f /etc/systemd/system/Sync.service ] && echo "Service loaded: Sync" && systemctl enable Sync
[ ! -f /etc/systemd/system/Screen.service ] && echo "Service loaded: Screen" && systemctl enable Screen && systemctl start Screen

echo "Setting permissions..."
echo ""
sudo chown -R mrminer:mrminer /root/mrminer/*
sudo chown -R mrminer:mrminer /home/mrminer/*
sudo chown -R root:root /etc/*

echo "Finished!"
echo ---------------------------
echo ">> Please REBOOT to apply changes of new version."
echo ---------------------------
sync
sleep 3
exit 0