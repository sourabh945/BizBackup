param($local_name,$remote_name,$code,$logs_file,$fails_file)

if ($code){
	echo "[ Done ] $local_name ----> $remote_name"
	echo "[ Done ] $local_name ----> $remote_name" | Out-File -FilePath "$logs_file" -Append
}
else {
	echo "[Fail] $local_name --X--> $remote_name"
	echo "[ Fail ] $local_name --X--> $remote_name" | Out-File -FilePath "$logs_file" -Append
	echo "[ Fails ] $local_name --X--> $remote_name" | Out-File -FilePath "$fails_file" -Append
}