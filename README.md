# EasyBWT-server-client

This is a small package with the purpose of computing Burrows-Wheeler transformations
of DNA sequences.
You will be able to host a server able to accept requests from a client using the command prompt.
In this folder you will find 3 scripts: **EasyBWT.py** is the script for the computation of the BWT and its reversion 
and in principle it could be used all for non-DNA strings but the server; **server.py** is the script that will make 
you able to host and handle requests from clients using parallel computing; **client.py** is the script used by the 
final user on the command line to request trasformation or decription of BWTs.
Note that you will need a python version greater than 3.10 for this program to work.

# SERVER SETUP:
1) Make sure that server.py is in the same folder as EasyBWT.py
2) If *config.txt* is not in the folder you can manually create it or run the server and it will be
created automatically by it
3) In config.txt modify the host to your custom IP address (default: localhost), you can also choose a
custom port (default: 16384), just be sure that it is an open port on your router.
4) The terminator character is "#" because "$" was messing with Windows Powershell but you can choose to use the "$" by
modifying the variable *terminator* in EasyBWT.py, just be aware that it needs to be a non-alphabetic character.
5) Within your shell go to the folder containing the scripts and start the server with the command:
"python server.py", your server is now on and waiting for clients to connect and make requests.

# CLIENT USAGE: 
Note that **client.py** does not need to be in the same folder as server.py.
The client will allow you to connect to a server with by specifying host and port then you can choose to transform a DNA
sequence in its BWT by using the option -t/-transform or to reverse a BWT with -r/-reverse and optionally you can choose
to save the output by using -s/-save. The **output.txt** file will be saved in the same folder of the client.
If you want you can provide the path of a fasta or txt file containing the sequence you want to transform/reverse, if 
provided with a fasta file be sure that it has a header line if not add at the start of the file ">some_text" and save it.
Note that the options must be provided in the order host-port-trasform/reverse-save otherwise the program will not work.

Examples:

1) **python client.py localhost 16384 -t CAGAGCTCATGAC -save**

This line will connect to the ip localhost on port 16384, transform the sequence in BWT and save the output
output: CGCGCA#TGTAACA

2) **python client.py localhost 16384 -reverse CGCGCA#TGTAACA -s**

This will reverse the BWT and save the output in a file.
output: CAGAGCTCATGAC#

3) **python client.py localhost 16384 -t your_dir/wuhan.fasta**

This will read the file wuhan.fasta and compute the BWT, if the file is in the same folder as client.py you can just
write wuhan.fasta. This command won't save the output in a file

4) **python client.py localhost 16384 -r output.txt -save**

This command will take the output.txt file in the same folder as the client and reverse the BWT then save again the new
output in the file output.txt.

