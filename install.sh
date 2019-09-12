#!/bin/bash

cd /home/lsminer/lsminer

sync

echo ""
echo "Lsminer is being configured"
echo ---------------------------
echo ""
echo "Files copying..."
echo ""
cp -f /home/lsminer/lsminer/etc/minerscreen.desktop /home/lsminer/.config/autostart/minerscreen.desktop
cp -f /home/lsminer/lsminer/etc/wallpaper.jpg /home/lsminer/wallpaper.jpg
sudo cp -f /home/lsminer/lsminer/etc/prepare.service /etc/systemd/system/prepare.service
sudo cp -f /home/lsminer/lsminer/etc/miner.service /etc/systemd/system/miner.service
sudo cp -f /home/lsminer/lsminer/etc/redline.service /etc/systemd/system/redline.service
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