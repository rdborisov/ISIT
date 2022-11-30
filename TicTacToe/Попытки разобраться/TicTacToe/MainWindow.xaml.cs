using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Controls;
using System.Windows;
using System.Windows.Form;

namespace WindowsFormsApplication1
{
    public partial class Form1 : Form
    {
        string name;
        bool pc = false;
        int hod = 1;
        bool turn = true; //true = x turn, false=y turn
        int turn_count = 0;
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }
        public void check()
        {

            {

                Random rnd = new Random();
                int p = rnd.Next(0, 8);
                if ((pc == true) || (name != A1.Text) || (name != A2.Text) || (name != A3.Text)
                   || (name != B1.Text) || (name != B2.Text) || (name != B3.Text) || (name != C1.Text)
                   || (name != C2.Text) || (name != C3.Text))
                {
                    switch (p)
                    {
                        case 0:
                            A1.Text = "O";
                            A1.Enabled = false;
                            turn_count++;
                            break;
                        case 1:
                            A2.Text = "O";
                            A2.Enabled = false;
                            turn_count++;
                            break;
                        case 2:
                            A3.Text = "O";
                            A3.Enabled = false;
                            turn_count++;
                            break;
                        case 3:
                            B1.Text = "O";
                            B1.Enabled = false;
                            turn_count++;
                            break;
                        case 4:
                            B2.Text = "O";
                            B2.Enabled = false;
                            turn_count++;
                            break;
                        case 5:
                            B3.Text = "O";
                            B3.Enabled = false;
                            turn_count++;
                            break;
                        case 6:
                            C1.Text = "O";
                            C1.Enabled = false;
                            turn_count++;
                            break;
                        case 7:
                            C2.Text = "O";
                            C2.Enabled = false;
                            turn_count++;
                            break;
                        case 8:
                            C3.Text = "O";
                            C3.Enabled = false;
                            turn_count++;
                            break;
                    }
                }

            }
        }



        private void button_click(object sender, EventArgs e)
        {
            Button b = (Button)sender;
            if (turn)
                b.Text = "X";
            if (!turn)
                b.Text = "O";
            pc = true;
            name = (sender as Button).Name;
            label1.Text = name + label1.Text;
            b.Enabled = false;
            turn_count++;
            label1.Text = turn_count.ToString();
            checkwinner();
            check();

        }
        private void checkwinner()
        {
            bool it_is_win = false;
            foreach (Control c in Controls)
            {
                if ((A1.Text == B1.Text) && (B1.Text == C1.Text) && (!A1.Enabled))

                    it_is_win = true;

                if ((B1.Text == B2.Text) && (B2.Text == B3.Text) && (!B1.Enabled))

                    it_is_win = true;

                if ((C1.Text == C2.Text) && (C2.Text == C3.Text) && (!C1.Enabled))

                    it_is_win = true;


                if ((A1.Text == B1.Text) && (B1.Text == C1.Text) && (!A1.Enabled))

                    it_is_win = true;

                else if ((A2.Text == B2.Text) && (B2.Text == C2.Text) && (!A2.Enabled))

                    it_is_win = true;

                else if ((A3.Text == B3.Text) && (B3.Text == C3.Text) && (!A3.Enabled))

                    it_is_win = true;


                else if ((A1.Text == B2.Text) && (B2.Text == C3.Text) && (!A1.Enabled))

                    it_is_win = true;

                else if ((A3.Text == B2.Text) && (B2.Text == C1.Text) && (!C1.Enabled))

                    it_is_win = true;

                if (it_is_win)
                {
                    disableButton();
                    String winner = "";
                    if (turn)
                        winner = "X";
                    if (!turn)
                        winner = "O";

                    MessageBox.Show(winner + " wins");
                }
                else
                {
                    if (turn_count == 9)
                        MessageBox.Show("Draw");
                }
            }
        }
        private void disableButton()
        {
            try
            {
                foreach (Control c in Controls)
                {
                    Button b = (Button)c;
                    b.Enabled = false;

                }
            }
            catch { }
        }

        private void новаяИграToolStripMenuItem_Click(object sender, EventArgs e)
        {
            turn = true;
            turn_count = 0;

            try
            {
                foreach (Control c in Controls)
                {
                    Button b = (Button)c;
                    b.Enabled = true;
                    b.Text = "";

                }
            }
            catch { }
        }
    }
}
