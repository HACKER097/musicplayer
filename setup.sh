#!/usr/bin/bash
pip3 install -r requirements.txt
HOME=`echo ~`
echo ENTER COMPLETE PATH TO MUSIC FOLDER : 
read FOLDER
cp main.py $FOLDER/main.py
echo "alias muicplayer='cd ~/Music; python3 main.py; cd ~/'" >> $HOME/.bashrc      
clear
echo restart bash and type "musicplayer" to start
echo up, down to gavigate, enter to play, space to pause/unpause
