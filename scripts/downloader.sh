#!/bin/bash

if [ $1 -eq 0 ]; then

    echo "[ Downloading ] [ Done ] $2 <---- $3" >> "$4"

else

    echo echo "[ Downloading ] [ Fail ] $2 <--x-- $3" >> "$4"

    echo "$1 <--x-- $2" >> "$5"

fi