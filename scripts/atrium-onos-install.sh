#!/bin/sh
#
# Script to install pre-requisites for Atrium in Ubuntu 14.04
# Assumes the caller has sudo privileges.
# Still requires interaction to accept the Oracle license
#
# Assumes atrium-onos is checked out in top level directory

cd ~

[ -f ~/.atrium_setup_done ] && \
  echo "Script already run. Remove .atrium_setup_done and re-run" && \
  return

touch ~/.atrium_setup_done

echo "Setting up system for Atrium-ONOS development"
sudo apt-get update
sudo apt-get install openssh-server -y
sudo apt-get install git -y

[ -d ~/atrium-onos ] || \
  cd ~ && git clone https://github.com/dtalayco/atrium-onos.git

sudo apt-get install software-properties-common -y
sudo add-apt-repository ppa:webupd8team/java -y
sudo apt-get update
echo "Installing Java"
sudo apt-get install oracle-java8-installer oracle-java8-set-default -y
sudo apt-get install maven -y
mkdir -p Applications
mkdir -p Downloads
git clone https://gerrit.onosproject.org/onos
echo "source ~/onos/tools/dev/bash_profile" >> ~/.bash_aliases
# And do it for this shell
source ~/onos/tools/dev/bash_profile
echo "Here are some important env variables (sanity check)"
echo ONOS_ROOT $ONOS_ROOT
echo KARAF_ROOT $KARAF_ROOT
echo JAVA_HOME $JAVA_HOME

# This sets up the configuration files such as sdnip.json and the cell file
~/atrium-onos/config/install.py
cell atriumbgp

echo "Building ONOS"
# Run the config install script again as karaf clean may remove some files
~/atrium-onos/config/install.py
cd ~/onos && mvn clean install

local_ip=`~/atrium-onos/scripts/local_ip.py`
echo "Setting up Karaf with local IP $local_ip"
onos-setup-karaf clean $local_ip
