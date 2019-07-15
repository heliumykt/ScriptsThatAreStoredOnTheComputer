using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Threading;

namespace GameClientTcpTest
{
    class Program
    {
        static Socket socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream,ProtocolType.Tcp);
        static string nick;

        static void Main(string[] args)
        {
            socket.Connect("127.0.0.1",904);
            Thread thread = new Thread(inputMessage);
            thread.Start();
            while(true){
                string message="0";
                ConsoleKeyInfo input = Console.ReadKey(true);
                if(input.Key.ToString()=="W") message = "2";
                else if(input.Key.ToString()=="S") message = "4";
                if(message=="2"||message=="4"){
                Console.Clear();
                Thread.Sleep(200);
                byte[] buffer = new byte [message.Length];
                buffer = Encoding.ASCII.GetBytes(nick+message);
                socket.Send(buffer);
                }
            }
        }
        static void inputMessage(){
            int y=15;
            int x=1;
            int y1=15;
            int x1=30;
            int xrange=30;
            int yrange=30;
            Console.WriteLine("Введи ник");
            nick = Console.ReadLine();
            while(true){
                byte[] buffer2 = new byte[1024];
                int size = socket.Receive(buffer2);
                Console.Clear();
                string outText = Encoding.ASCII.GetString(buffer2,0,size);
                string xy="";
                string nickChek = "";
                int j=0;
                foreach (char i in outText){
                    j++;
                    if(j==outText.Length){
                        xy=i.ToString();
                    }
                    else{
                        nickChek= nickChek + i.ToString();
                    }
                }
                if (xy=="4" && nick==nickChek) y++;
                else if (xy=="4" && nick!=nickChek) y1++;
                if (xy=="2" && nick==nickChek) y--;
                else if (xy=="2" && nick!=nickChek) y1--;

                if(y==0) y=1;
                if(y==yrange+1) y=30;
                if(y1==0) y1=1;
                if(y1==yrange+1) y1=30;

                for (int m=1;m<=yrange;m++){
                    for (int n=1;n<=xrange;n++){
                        if (x==n && y==m) Console.Write("Я");
                        if (x1==n && y1==m) Console.Write("В");
                        else Console.Write(" ");      
                    }
                    Console.WriteLine();
                }
            }
        }
    }
}