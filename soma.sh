#!/bin/bash

amixer controls
# numid=1 PCM playback volume 3 route
sudo amixer cset numid=3 1
sudo amixer cset numid=1 85%
amixer cget numid=1
sudo alsactl store
# /var/lib/alsa/asound.state

mpc clear
mpc load http://somafm.com/spacestation.pls
mpc load http://somafm.com/missioncontrol.pls
mpc load http://somafm.com/deepspaceone.pls
mpc load http://somafm.com/groovesalad.pls
mpc load http://somafm.com/seventies.pls
mpc volume 80
mpc stop

