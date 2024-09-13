
### scripts paths 

Paths = {'upload_bash':'./scripts/uploader.sh','upload_ps':'./scripts/uploader.ps1','downlaod_bash':'./scripts/downloader.sh','download_ps':'./scripts/downloader.ps1'}


### scripts 

scripts = {
    # script for data output and logging in linux
    'upload_bash':"""#!/bin/bash 

if [ $3 -eq 0 ]; then 

    echo ""

    echo "[ Done ] $1 -----> $2"

    echo "[ Uploading ] [ Done ] $1 -----> $2" >> "$4"

else

    echo ""

    echo "[ Fail ] $1 --x--> $2" 

    echo "[ Uploading ] [ Fail ] $1 --x--> $2" >> "$4"

    echo "$1 --x--> $2" >> "$5"

fi

""",
# script for data output and logging in windows
'upload_ps' : """param($local_name,$remote_name,$code,$logs_file,$fails_file)

if ($code){
	echo "[ Done ] $local_name ----> $remote_name"
	echo "[ Uploading ] [ Done ] $local_name ----> $remote_name" | Out-File -FilePath "$logs_file" -Append
}
else {
	echo "[Fail] $local_name --x--> $remote_name"
	echo "[ Uploading ] [ Fail ] $local_name --x--> $remote_name" | Out-File -FilePath "$logs_file" -Append
	echo "$local_name --x--> $remote_name" | Out-File -FilePath "$fails_file" -Append
}""",
# script for download logging in linux 
'download_bash' : """#!/bin/bash

if [ $1 -eq 0 ]; then

    echo "[ Downloading ] [ Done ] $2 <---- $3" >> "$4"

else

    echo echo "[ Downloading ] [ Fail ] $2 <--x-- $3" >> "$4"

    echo "$1 <--x-- $2" >> "$5"

fi""",
'download_ps' : """param($local_name,$remote_name,$code,$logs_file,$fails_file)

if ($code){
	echo "[ Downloading ] [ Done ] $local_name <---- $remote_name" | Out-File -FilePath "$logs_file" -Append
}
else {

	echo "[ Downloading ] [ Fail ] $local_name <--x-- $remote_name" | Out-File -FilePath "$logs_file" -Append
	echo "$local_name <--x-- $remote_name" | Out-File -FilePath "$fails_file" -Append
}""" 

}



