import socket
import sys

class Client:

    def __init__(self):
        #storing the user inputted parameters
        self.host, self.port, self.method, self.query = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]

        #handling the optional parameter for saving the output in a file
        if len(sys.argv) == 6:
            self.save = sys.argv[5]
        else:
            self.save = None

        self.end = b"\0"
        self.max_bytes = 8192
        self.main()

    def main(self):
        #create the socket object for the client and handle all the operation
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            #if the query is a fasta file extract the sequence to process
            if self.query.endswith(".fasta") or self.query.endswith(".txt"):
                self.query = self.handle_files(self.query)

            s.sendall(bytes(self.method + " " + self.query, "utf-8") + self.end)

            #verify the integrity of the recieved data
            total_data = []
            data = ''

            while True:
                data = s.recv(self.max_bytes)
                if self.end in data:
                    total_data.append(data[:data.find(self.end)])
                    break
                total_data.append(data)

            data = str(b''.join(total_data), "utf-8")

        #print the final output on the screen
        print("\nOUTPUT: "+data+"\n")

        #store output in a txt file if requested by the user with -s
        if self.save:
            if self.save == "-s" or self.save == "-save":
                with open("output.txt", "w") as f:
                    f.write(data)
                print("Output saved in output.txt")
            else:
                print("WARNING: invalid save option, output will not be saved")

    #read the file, skip the header if it is a fasta and join the lines
    def handle_files(self, file):
        data = []
        if file.endswith(".fasta"):
            with open(file, "r") as f:
                f.readline()
                for line in f.readlines():
                    line = line.strip("\n")
                    data.append(line)
            data = "".join(data)
        elif file.endswith(".txt"):
            with open(file, "r") as f:
                for line in f.readlines():
                    line = line.strip("\n")
                    data.append(line)
            data = "".join(data).strip("")
        return data

#run the client
if __name__ == "__main__":
    Client()