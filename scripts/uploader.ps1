param($local_name,$remote_name,$code,$logs_file,$fails_file)

if ($code){
	echo "[ Done ] $local_name ----> $remote_name"
	echo "[ Uploading ] [ Done ] $local_name ----> $remote_name" | Out-File -FilePath "$logs_file" -Append
}
else {
	echo "[Fail] $local_name --x--> $remote_name"
	echo "[ Uploading ] [ Fail ] $local_name --x--> $remote_name" | Out-File -FilePath "$logs_file" -Append
	echo "$local_name --x--> $remote_name" | Out-File -FilePath "$fails_file" -Append
}