using System;
using System.Windows;

namespace TestWPF
{
    class Program
    {
        [STAThread]
        static void Main(string[] args)
        {
            Console.WriteLine("Starting WPF window...");
            
            Window window = new Window
            {
                Title = "Test Window",
                Width = 400,
                Height = 300,
                Visibility = Visibility.Visible
            };
            
            Application app = new Application();
            app.Run(window);
            
            Console.WriteLine("Window closed.");
        }
    }
}