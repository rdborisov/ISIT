using System;
using System.Threading;

namespace TIC_TAC_TOE
{
    class Game
    {
        static char[] field = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' };
        static int player = 1;
        static int choice;
        static int flag = 0;
        static void Main(string[] args)
        {
            do
            {
                Console.Clear();
                if (player % 2 == 0)
                {
                    Console.WriteLine("0 Chance");
                }
                else
                {
                    Console.WriteLine("X Chance");
                }
                Console.WriteLine("\n");
                PleyField();
                choice = int.Parse(Console.ReadLine());
                if (field[choice] != 'X' && field[choice] != 'O')
                {
                    if (player % 2 == 0)
                    {
                        field[choice] = 'O';
                        player++;
                    }
                    else
                    {
                        field[choice] = 'X';
                        player++;
                    }
                }
                else
                {
                    Thread.Sleep(2000);
                }
                flag = CheckWin();
               

            }
            while (flag != 1 && flag != -1);
            Console.Clear();
            PleyField();
            if (flag == 1)
            {
                Console.WriteLine($"{field[choice]} has won", (player % 2) + 1);
            }
            else
            {
                Console.WriteLine("Draw");
            }
            Console.ReadLine();
        }
        private static void PleyField()
        {
            Console.WriteLine("     |     |      ");
            Console.WriteLine("  {0}  |  {1}  |  {2}", field[7], field[8], field[9]);
            Console.WriteLine("_____|_____|_____ ");
            Console.WriteLine("     |     |      ");
            Console.WriteLine("  {0}  |  {1}  |  {2}", field[4], field[5], field[6]);
            Console.WriteLine("_____|_____|_____ ");
            Console.WriteLine("     |     |      ");
            Console.WriteLine("  {0}  |  {1}  |  {2}", field[1], field[2], field[3]);
            Console.WriteLine("     |     |      ");
        }
        private static int CheckWin()
        {
            if (field[1] == field[2] && field[2] == field[3])
            {
                return 1;
            }
            else if (field[4] == field[5] && field[5] == field[6])
            {
                return 1;
            }
            else if (field[6] == field[7] && field[7] == field[8])
            {
                return 1;
            }
            else if (field[1] == field[4] && field[4] == field[7])
            {
                return 1;
            }
            else if (field[2] == field[5] && field[5] == field[8])
            {
                return 1;
            }
            else if (field[3] == field[6] && field[6] == field[9])
            {
                return 1;
            }
            else if (field[1] == field[5] && field[5] == field[9])
            {
                return 1;
            }
            else if (field[3] == field[5] && field[5] == field[7])
            {
                return 1;
            }
            else if (field[1] != '1' && field[2] != '2' && field[3] != '3' && field[4] != '4' && field[5] != '5' && field[6] != '6' && field[7] != '7' && field[8] != '8' && field[9] != '9')
            {
                return -1;
            }
            else
            {
                return 0;
            }
        }
    }

    class AI
    { 
        public static void RandomAI(char[] field)
        {

        }
    
    }
}