#!/bin/bash

# source ./utils.sh
# find_distro_name

wget https://github.com/jonathanmarvens/argtable2/archive/master.zip
unzip master.zip
cd argtable2-master
if [[ $OS == *"UBUNTU"* ]]; then
	sudo apt-get install libtool
	sudo autoreconf --install
elif [[ $OS == *"DEBIAN"* ]]; then
	su -c "apt-get install libtool"
	su -c "autoreconf --install"
fi
autoconf configure.ac
./configure
make
if [[ $OS == *"UBUNTU"* ]]; then
	sudo make install
elif [[ $OS == *"DEBIAN"* ]]; then
	su -c "make install"
fi

wget http://www.clustal.org/omega/clustal-omega-1.2.4.tar.gz
tar -xvf clustal-omega-1.2.4.tar.gz
cd clustal-omega-1.2.4
./configure
make
if [[ $OS == *"UBUNTU"* ]]; then
	sudo make install
	sudo ldconfig
elif [[ $OS == *"DEBIAN"* ]]; then
	su -c "make install"
	su -s /usr/sbin/ldconfig
fi