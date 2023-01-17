$FilePath = 'D:\Users\jon\Nextcloud\!System Folders\Documents\Source\ProcessID\bin\Release\ProcessID.dll'
$File = [System.IO.File]::ReadAllBytes($FilePath)
$blob = [System.Convert]::ToBase64String($File)
echo @"
`$blob = '$blob'
"@ | Out-File 'D:\Users\jon\Nextcloud\!System Folders\Documents\Source\ProcessID\bin\Release\ProcessIDBlob.ps1'