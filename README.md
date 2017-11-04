Family box
==========

Collection of tools to install a family raspberry = a minimalist media center managed through a tablet.

It includes:
- a video player (omxplayer)
- a wifi hotspot to connect your device
- a web interface to manage the mediacenter


Install
-------
1. Get latest raspbian image: https://www.raspberrypi.org/downloads/raspbian/
2. Write the image to an sd card: https://www.raspberrypi.org/documentation/installation/installing-images/README.md
3. Create a '/boot/ssh' file to enable ssh on reboot (warning: do it if you are on a secure network only)
4. Boot

Once booted:
1. Install ansible and git: ```apt-get install ansible git```
2. Configure your system. Copy inventory.sample as inventory then edit it.
3. Get the family_box project: ```git clone https://github.com/seb4stien/family_box.git```
4. Run the ansible playbook: ```ansible-playbook -i inventory -c local local.yml --check``` (remove the --check when ok)
