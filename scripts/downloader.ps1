param($local_name,$remote_name,$code,$logs_file,$fails_file)

if ($code){
	echo "[ Downloading ] [ Done ] $local_name <---- $remote_name" | Out-File -FilePath "$logs_file" -Append
}
else {

	echo "[ Downloading ] [ Fail ] $local_name <--x-- $remote_name" | Out-File -FilePath "$logs_file" -Append
	echo "$local_name <--x-- $remote_name" | Out-File -FilePath "$fails_file" -Append
}