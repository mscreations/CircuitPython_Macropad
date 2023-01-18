$FilePath = 'D:\Users\jon\Nextcloud\!System Folders\Documents\Source\New Work Macropad codebase\MSCreations\bin\Release\MSCreations.dll'
$File = [System.IO.File]::ReadAllBytes($FilePath)
$blob = [System.Convert]::ToBase64String($File)
Write-Output @"
`$blob = '$blob'
"@ | Out-File 'D:\Users\jon\Nextcloud\!System Folders\Documents\Source\New Work Macropad codebase\MSCreationsBlob.ps1'