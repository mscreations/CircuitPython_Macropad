using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace MSCreations
{
    public class Client
    {
        public Client() 
        {
        }

        public static void Write(string message, int port = 1200)
        {
            string address = "127.0.0.1";

            try
            {
                TcpClient client = new TcpClient(address, port);
                byte[] data = Encoding.ASCII.GetBytes(message);

                NetworkStream stream = client.GetStream();
                stream.Write(data, 0, data.Length);
            }
            catch (Exception e)
            {
                MessageBox.Show("Exception:\n\n" + e.ToString(), "Exception occured", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
