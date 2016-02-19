using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Data.SQLite;
using System.IO;
using System.IO.Ports;

namespace Testestorone
{
    public partial class Form1 : Form
    {
        public void refSensors()
        {

            //(node INT, lasttemp REAL, lasthumidity REAL, customname TEXT)

            DataTable table = new DataTable();

            table.Columns.Add("Node", typeof(int));
            table.Columns.Add("Last temperature", typeof(string));
            table.Columns.Add("Last humidity", typeof(string));
            table.Columns.Add("Nickname", typeof(string));

            SQLiteConnection m_dbConnection;
            m_dbConnection =
            new SQLiteConnection("Data Source=data.sqlite;Version=3;datetimeformat=CurrentCulture");
            m_dbConnection.Open();

            string sql = "select node, lasttemp, lasthumidity, customname from sensors";

            SQLiteCommand command = new SQLiteCommand(sql, m_dbConnection);

            SQLiteDataReader reader = command.ExecuteReader();

            while (reader.Read())
            {

                table.Rows.Add(reader["node"], reader["lasttemp"], reader["lasthumidity"], reader["customname"]);
            }

            m_dbConnection.Close();

            dataGridView1.DataSource = table;

            dataGridView1.Columns[0].AutoSizeMode = DataGridViewAutoSizeColumnMode.AllCells;
            dataGridView1.Columns[1].AutoSizeMode = DataGridViewAutoSizeColumnMode.AllCells;
            dataGridView1.Columns[2].AutoSizeMode = DataGridViewAutoSizeColumnMode.AllCells;
            dataGridView1.Columns[3].AutoSizeMode = DataGridViewAutoSizeColumnMode.Fill;
        }

        public Form1()
        {
            InitializeComponent();

            if (!File.Exists("data.sqlite"))
            {
                SQLiteConnection.CreateFile("data.sqlite");
                SQLiteConnection m_dbConnection;
                m_dbConnection =
                new SQLiteConnection("Data Source=data.sqlite;Version=3;");
                m_dbConnection.Open();

                string sql = "CREATE TABLE sensors (node INT, lasttemp REAL, lasthumidity REAL, customname TEXT)";

                SQLiteCommand command2 = new SQLiteCommand(sql, m_dbConnection);

                command2.ExecuteNonQuery();

                m_dbConnection.Close();
            }

            refSensors();
        }

        private void comboBox1_MouseClick(object sender, MouseEventArgs e)
        {
            comboBox1.Items.Clear();
            foreach (string s in SerialPort.GetPortNames())
            {
                comboBox1.Items.Add(s);
            }  
        }

        private bool connected = false;

        private void button1_Click(object sender, EventArgs e)
        {
            if (comboBox1.SelectedIndex > -1 && connected == false)
            {
               try
                {
                    serialPort1.BaudRate = 57600;
                    serialPort1.PortName = comboBox1.SelectedItem.ToString();
                 
                    serialPort1.Open();

                    this.Text = "Testestorone - Connected to " + comboBox1.SelectedItem.ToString();
                    connected = true;
                    button1.Text = "Disconnect";

               }
                catch (Exception ex)
               {
                    this.Text = "Testestorone - Error connecting";
                   richTextBox1.AppendText(ex.Message.ToString());
               }
            }
            else
            {
                serialPort1.Close();
                connected = false;
                this.Text = "Testestorone - Disconnected";
                button1.Text = "Connect";
            }
        }

        public string RxString = "";

        private void serialPort1_DataReceived(object sender, SerialDataReceivedEventArgs e)
        {
            
            try
                {
                    RxString = serialPort1.ReadTo("\n");
                    this.Invoke(new EventHandler(DisplayText));
                }
            catch
                { 
            
                }

        }

        private void DisplayText(object sender, EventArgs e)
        {
            richTextBox1.AppendText(RxString);
            string RequestedNode = string.Empty;
            string Success = string.Empty;
            string Humidity = string.Empty;
            string Temperature = string.Empty;

            if (RxString.Contains("RQ"))
            {
                RequestedNode = RxString.Split(';')[1];
                Success = RxString.Split(';')[3];

                

                if (Int32.Parse(Success) == 1)
                {
                    SQLiteConnection m_dbConnection;
                    m_dbConnection =
                    new SQLiteConnection("Data Source=data.sqlite;Version=3;");
                    m_dbConnection.Open();

                    //(node INT, lasttemp REAL, lasthumidity REAL, customname TEXT)
                    string sql = @"INSERT INTO sensors(node,lasttemp, lasthumidity, customname) 
                                SELECT " + RequestedNode + @", 0,0,'-'  
                                WHERE NOT EXISTS(SELECT 1 FROM sensors WHERE node = " + RequestedNode + @");";

                    SQLiteCommand command2 = new SQLiteCommand(sql, m_dbConnection);

                    command2.ExecuteNonQuery();

                    m_dbConnection.Close();

                    refSensors();
                }
            }

            if (RxString.Contains("ND"))
            {
                RequestedNode = RxString.Split(';')[1];
                Humidity = RxString.Split(';')[3];
                Temperature = RxString.Split(';')[5];



                
                    SQLiteConnection m_dbConnection;
                    m_dbConnection =
                    new SQLiteConnection("Data Source=data.sqlite;Version=3;");
                    m_dbConnection.Open();

                    //(node INT, lasttemp REAL, lasthumidity REAL, customname TEXT)
                    string sql = @"Update sensors 
                                SET lasttemp = '"+Temperature+"', lasthumidity = '"+Humidity+"' WHERE node = '"+RequestedNode+"'";

                    SQLiteCommand command2 = new SQLiteCommand(sql, m_dbConnection);

                    command2.ExecuteNonQuery();

                    m_dbConnection.Close();

                    refSensors();
                
            }



            richTextBox1.SelectionStart = richTextBox1.Text.Length;
            richTextBox1.ScrollToCaret();
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            serialPort1.Close();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            richTextBox1.Text = "";
        }

        private void dataGridView1_CellContentDoubleClick(object sender, DataGridViewCellEventArgs e)
        {
            DataGridViewRow row = dataGridView1.CurrentCell.OwningRow;
            string value = row.Cells["Node"].Value.ToString();
            NameSensor nm = new NameSensor();
            nm.ShowDialog();

            if (nm.DialogResult == DialogResult.OK)
            {
                SQLiteConnection m_dbConnection;
                m_dbConnection =
                new SQLiteConnection("Data Source=data.sqlite;Version=3;");
                m_dbConnection.Open();

                //(node INT, lasttemp REAL, lasthumidity REAL, customname TEXT)
                string sql = @"Update sensors 
                                SET customname = '"+Form1.SetName+"' WHERE node = '" + value + "'";

                SQLiteCommand command2 = new SQLiteCommand(sql, m_dbConnection);

                command2.ExecuteNonQuery();

                m_dbConnection.Close();

                refSensors();
            }
        }

        public static string SetName { get; set; }

    }
}
