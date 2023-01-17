using System.Linq;
using System.Management;

namespace ProcessID
{
    public class SerialHelp
    {
        public static string GetMacropadDataSerialPort()
        {
            foreach (string Port in System.IO.Ports.SerialPort.GetPortNames())
            {
                ManagementObjectSearcher searcher = new ManagementObjectSearcher("SELECT * FROM Win32_PnPEntity WHERE Name LIKE '%" + Port + "%'");
                ManagementObject mo = searcher.Get().OfType<ManagementObject>().FirstOrDefault();
                object[] args = new object[] { new string[] { "DEVPKEY_Device_BusReportedDeviceDesc" }, null };
                mo.InvokeMethod("GetDeviceProperties", args);
                ManagementBaseObject[] mbos = (ManagementBaseObject[])args[1];
                if (mbos.Length > 0)
                {
                    PropertyData data = mbos[0].Properties.OfType<PropertyData>().FirstOrDefault(p => p.Name == "Data");
                    if (data != null && data.Value.ToString().Contains("CDC2"))
                    {
                        return Port;
                    }
                }
            }
            return null;
        }
    }
}
