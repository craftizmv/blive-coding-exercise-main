#!/usr/bin/env bash

curl https://mise.run | sh
echo "export PATH=$PATH:$HOME/.local/bin:$HOME/.local/share/mise/bin" >> /root/.bashrc
source /root/.bashrc
echo 'eval "$(mise activate bash)"' >> ~/.bashrc

bash -ci "$(wget -qO - 'https://shlink.makedeb.org/install')"

wget -qO - 'https://proget.makedeb.org/debian-feeds/prebuilt-mpr.pub' | gpg --dearmor | tee /usr/share/keyrings/prebuilt-mpr-archive-keyring.gpg 1> /dev/null
echo "deb [arch=all,$(dpkg --print-architecture) signed-by=/usr/share/keyrings/prebuilt-mpr-archive-keyring.gpg] https://proget.makedeb.org prebuilt-mpr $(lsb_release -cs)" | tee /etc/apt/sources.list.d/prebuilt-mpr.list
apt-get update
apt-get install -y just

bash -ci "$(mise install)"

