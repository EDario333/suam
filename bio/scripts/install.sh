#!/bin/bash

upgrade_sys() {
	if [[ $OS == *"UBUNTU"* ]]; then
		sudo apt update
		sudo apt upgrade -y
	elif [[ $OS == *"DEBIAN"* ]]; then
		su -c "apt update && apt upgrade -y"
	fi
}

install_deps() {
	if [[ $OS == *"UBUNTU"* ]]; then
		sudo apt install -y libffi-dev libx11-dev autoconf libtool
	elif [[ $OS == *"DEBIAN"* ]]; then
		su -c "apt install -y libffi-dev libx11-dev autoconf libtool"
	fi
}

clean() {
	rm -rf argtable2-master
	rm -rf clustal-omega-1.2.4
	rm -f clustal-omega-1.2.4.tar.gz
	rm -f muscle3.8.31_src.tar.gz
	rm -f master.zip
}

chmod +x utils.sh
chmod +x clustalo.sh
chmod +x muscle.sh

source ./utils.sh
find_distro_name
upgrade_sys
install_deps
mkdir 3rd
cd 3rd
./clustalo.sh
./muscle.sh
clean