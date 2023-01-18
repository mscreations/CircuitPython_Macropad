using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace MSCreations
{
    public class Server
    {
        private readonly TcpListener listener;
        private readonly byte[] buffer;
        private readonly IPAddress address;
        private readonly int port;
        private readonly Queue<string> queue;
        private Thread thread;

        public bool DataAvailable => queue.Count > 0;

        public string ReadQueue() => queue.Dequeue();
        public Server(int port = 1200)
        {
            address = IPAddress.Parse("127.0.0.1");
            this.port = port;
            listener = new TcpListener(address, port);
            buffer = new byte[4096];
            queue = new Queue<string>();
        }

        public void Start()
        {
            listener.Start();
            thread = new Thread(new ThreadStart(ThreadTask))
            {
                IsBackground = true
            };
            thread.Start();
        }

        private void ThreadTask()
        {
            try
            {
                while (true)
                {
                    TcpClient client = listener.AcceptTcpClient();

                    NetworkStream stream = client.GetStream();

                    int i;

                    i = stream.Read(buffer, 0, buffer.Length);

                    if (i > 0)
                    {
                        queue.Enqueue(Encoding.ASCII.GetString(buffer, 0, i));
                    }
                    client.Close();
                }
            }
            catch (SocketException e)
            { 
                MessageBox.Show("Exception:\n\n" + e.ToString(), "Socket Exception", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

    }
}
