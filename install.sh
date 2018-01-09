#!/usr/bin/env bash

update(){
  # bypass: Could not get lock
  pkill apt-get

  # bypass: no installation candidate
  echo "deb http://http.kali.org/kali kali-rolling main contrib non-free" > /etc/apt/sources.list
  apt-get update
}

install(){
  # install requirements
  for i in `cat requirements.txt`
  do
     apt-get install $i -y
  done

  # clean up
  apt autoremove -y
}

# run
update
install
