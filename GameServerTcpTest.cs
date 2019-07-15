using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Threading;


namespace GameServerTcpTest
{
    class Program
    {
        static Socket socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        static Socket[] client = new Socket[2];
        static void Main(string[] args)
        {
            Thread thread1= new Thread(Server);
            Thread thread2= new Thread(Server1);
            socket.Bind(new IPEndPoint(IPAddress.Any,904));
            socket.Listen(2);
            client[0] = socket.Accept();
            Console.WriteLine("подрубалити");
            thread1.Start();
            client[1] = socket.Accept();
            Console.WriteLine("подрубалити");
            thread2.Start();
        }
        static void Server(){
            while(true){
                byte[] buffer = new byte[1024];
                int size1 = client[0].Receive(buffer);
                string outText1=Encoding.ASCII.GetString(buffer,0,size1);
                byte[] outEncod1 = new byte[outText1.Length];
                outEncod1 = Encoding.ASCII.GetBytes(outText1);
                client[0].Send(outEncod1);
                if (client[1]!=null) client[1].Send(outEncod1);
            }
        }
        static void Server1(){
            while(true){
                byte[] buffer1 = new byte[1024];
                int size = client[1].Receive(buffer1);
                string outText=Encoding.ASCII.GetString(buffer1,0,size);
                byte[] outEncod = new byte[outText.Length];
                outEncod = Encoding.ASCII.GetBytes(outText);
                client[1].Send(outEncod);
                client[0].Send(outEncod);
            }
        }
    }
}