try {
    $OldWindow = $null

    # Load DLL to retrieve process name. This is used because there is no good way to handle UWP processes
    #       like Calculator or Windows store otherwise.

    # This is how $blob is created.
    # $FilePath = "<Path to MSCreations.dll>"
    # $File = [System.IO.File]::ReadAllBytes($FilePath)
    # $blob = [System.Convert]::ToBase64String($File)

    # MSCreations.dll blob - Provides serial port detection and process identification
    . .\MSCreationsBlob.ps1
    [void][System.Reflection.Assembly]::Load([Convert]::FromBase64String($blob))

    $ComPort = [MSCreations.SerialHelp]::GetMacropadDataSerialPort()

    if (!$ComPort) {
        Write-Error 'Could not find MacroPad attached to system.'
        exit
    }

    Write-Host 'Found MacroPad on port ' -NoNewline
    Write-Host $ComPort -ForegroundColor Green

    $Port = [System.IO.Ports.SerialPort]::new($ComPort, 115200)
    # Enable DTR, otherwise Macropad will not detect that it is connected, even though it will receive data.
    # Absolutely necessary on versions 8.0.0-beta.4 and later as a fix was put in that makes it necessary to be
    # connected before allowing a read.
    $Port.DtrEnable = $true
    $Port.Open()

    while ($true) {
        try {
            while (!$Port.IsOpen) {
                for ($i = 5; $i -gt 0; $i--) {
                    Write-Host "Port disconnected. Retry in $i seconds.`r" -NoNewline
                    Start-Sleep 1
                }
                $Port.Open()
                if ($Port.IsOpen) {
                    Write-Host "                                       `r" -NoNewline
                }
            }
        }
        catch {
            continue
        }

        $Window = [MSCreations.UwpUtils]::GetActiveProcessName()

        if ($Window -ne $OldWindow) {
            try {
                $Port.WriteLine(('{0}' -f $Window))
                $Port.ReadLine()
            }
            catch {
                continue
            }

            $OldWindow = $Window
        }
        Start-Sleep 1
    }
}
catch {
    Write-Error "Exception occurred: $_"
}
finally {
    Write-Host 'Closing Serial port'
    $Port.Close()
    $Port.Dispose()
    $Port = $null
}
