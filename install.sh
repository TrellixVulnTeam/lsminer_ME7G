#!/bin/bash
sync

echo ""
echo "Lsminer is being configured"
echo ---------------------------
echo ""
echo "Files copying..."
echo ""
sudo cp -f /root/mrminer/etc/minerscreen.desktop /home/mrminer/.config/autostart/minerscreen.desktop
sudo cp -f /root/mrminer/etc/wallpaper.jpg /home/mrminer/wallpaper.jpg
sudo cp -f /root/mrminer/etc/prepare.service /etc/systemd/system/prepare.service
sudo cp -f /root/mrminer/etc/miner.service /etc/systemd/system/miner.service
sudo cp -f /root/mrminer/etc/redline.service /etc/systemd/system/redline.service
sync
sleep 1

echo "Activating services..."
echo ""
[ ! -f /etc/systemd/system/prepare.service ] && echo "Service loaded: prepare" && systemctl enable prepare
[ ! -f /etc/systemd/system/miner.service ] && echo "Service loaded: miner" && systemctl enable miner
[ ! -f /etc/systemd/system/redline.service ] && echo "Service loaded: redline" && systemctl enable redline

echo "Setting permissions..."
echo ""
sudo chown -R lsminer:lsminer /home/lsminer/*
sudo chown -R root:root /etc/*

echo "Finished!"
echo ---------------------------
echo ">> Please REBOOT to apply changes of new version."
echo ---------------------------
sync
sleep 3
exit 0