#!/bin/bash 

if [ $3 -eq 0 ]; then 

    echo ""

    echo "[ Done ] $1 -----> $2"

    echo "[ Uploading ] [ Done ] $1 -----> $2" >> "$4"

else

    echo ""

    echo "[ Fail ] $1 --X--> $2" 

    echo "[ Uploading ] [ Fail ] $1 --X--> $2" >> "$4"

    echo "$1 --X--> $2" >> "$5"

fi