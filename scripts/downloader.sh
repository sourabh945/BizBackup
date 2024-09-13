#!/bin/bash

if [ $3 -eq 0 ]; then

    echo "[ Downloading ] [ Done ] $1 <---- $2" >> "$4"

else

    echo echo "[ Downloading ] [ Fail ] $1 <--x-- $2" >> "$4"

    echo "$1 <--x-- $2" >> "$5"

fi