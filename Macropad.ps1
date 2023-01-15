if ($PSVersionTable.PSVersion.Major -gt 5) {
    # GetDeviceProperties is only available if running in Powershell 5.1.
    powershell.exe -noprofile -file $MyInvocation.MyCommand.Path
    exit
}

Add-Type @'
using System;
using System.Runtime.InteropServices;
using System.Text;
public class WinAPIs
{
    [DllImport("user32.dll", SetLastError=true, CharSet=CharSet.Auto)]
        public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll", SetLastError=true, CharSet=CharSet.Auto)]
        public static extern Int32 GetWindowThreadProcessId(IntPtr hWnd,out Int32 lpdwProcessId);
}
'@

$OldWindow = $null

foreach($Port in ([System.IO.Ports.SerialPort]::GetPortNames())) {
    $Desc = (Get-WmiObject Win32_PnPEntity | Where-Object Name -match "$Port").GetDeviceProperties('DEVPKEY_Device_BusReportedDeviceDesc').deviceProperties.Data
    # CDC2 is the usb_cdc.data serial port
    if ($Desc -match 'CDC2') {
        $ComPort = $Port
    }
}

if (!$ComPort) {
    Write-Error 'Could not find MacroPad attached to system.'
    exit
}

Write-Host 'Found MacroPad on port ' -NoNewline
Write-Host $ComPort -ForegroundColor Green

$Port = [System.IO.Ports.SerialPort]::new($ComPort, 38400)

try {
    while ($true) {
        if (!$Port.IsOpen) { $Port.Open() }

        $Window = [WinAPIs]::GetForegroundWindow()
        if ($Window -ne $OldWindow) {
            $Proc = $null
            [WinAPIs]::GetWindowThreadProcessId($Window, [ref]$Proc) | Out-Null
            $Process = Get-Process | Where-Object Id -EQ $Proc

            $Process | Select *

            $ProcessName = $Process.ProcessName

            # Handle calculator
            if (($Process.Name -eq 'ApplicationFrameHost') -and ($Process.MainWindowTitle -eq 'Calculator')) {
                $ProcessName = "calc"
            }

            $Port.WriteLine(('{0}' -f $ProcessName))
            $Port.ReadLine()

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
