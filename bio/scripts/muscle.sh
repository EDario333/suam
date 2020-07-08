#!/bin/bash

# source utils.sh
# find_distro_name

wget https://www.drive5.com/muscle/downloads3.8.31/muscle3.8.31_src.tar.gz
tar -xvf muscle3.8.31_src.tar.gz
cd muscle3.8.31/src
make
chmod +x muscle
if [[ $OS == *"UBUNTU"* ]]; then
	sudo ln -s $PWD/muscle /usr/local/bin/muscle
elif [[ $OS == *"DEBIAN"* ]]; then
	su -c "ln -s $PWD/muscle /usr/local/bin/muscle"
fi