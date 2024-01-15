import os
import socket
import multiprocessing
from EasyBWT import BWT, reverse_BWT

#NOTE: you need python 3.10 or greater to run this server

class Server:

    #initialize all the class variables
    def __init__(self):
        self.configs = self.handle_configs()
        self.host, self.port = self.configs["host"], self.configs["port"]
        self.max_bytes = 8192
        self.end = b"\0"
        self.terminator = "#"
        self.backlog = 100
        self.main()

    #run the server and handle the multiprocessing
    def main(self):
        #using the with statement context manager we don't need to call s.close()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(self.backlog)
            print(f"Listening on {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()
                print('Process', os.getpid(), 'got connection from', addr[0], "port", addr[1])
                process = multiprocessing.Process(target=self.handle_request, args=(conn,))
                process.daemon = True #to prevent orphan processes if the parent process is terminated
                process.start()

    #verify the integrity of the recieved data
    def recv_end(self, conn):
        total_data = []
        data = ''

        while True:
            data = conn.recv(self.max_bytes)
            if self.end in data:
                total_data.append(data[:data.find(self.end)])
                break
            total_data.append(data)
        return b''.join(total_data)

    #handles the request and do all the validation
    def handle_request(self, conn):
        data = str(self.recv_end(conn), "utf-8")
        method, data = data.split(" ")

        match method:
            case "-t" | "-transform":
                data, valid = self.validator(data, method)
                if valid:
                    data = BWT(data)
            case "-r" | "-reverse":
                data, valid = self.validator(data, method)
                if valid:
                    data = reverse_BWT(data)
            case other:
                data = "Error: Invalid Operation, type -t/-transform or -r/-reverse"

        conn.sendall(bytes(data, "utf-8") + self.end)
        conn.close()

    #check if the string given by the user is valid
    def validator(self, data, method):
        temp_data = data.upper()
        alphabet = f"{self.terminator}ACGT"
        data_len = len(data)
        valid_count = 0

        for letter in alphabet:
            valid_count += temp_data.count(letter)

        if valid_count != data_len:
            data = "Error: the string must be a DNA"
            return data, False

        match method:
            case "-t" | "-transform":
                if temp_data.count(self.terminator) > 0:
                    data = "Error: The string cannot contain any symbol"
                    return data, False
                else:
                    return data, True
            case "-r" | "-reverse":
                if temp_data.count(self.terminator) != 1:
                    data = f"Error: The string cannot contain more than one {self.terminator}"
                    return data, False
                else:
                    return data, True

    def handle_configs(self):
        #create the config file if it does not exist in the folder, initialize the options with a default value
        if not os.path.isfile("config.txt"):
            options = ["host = localhost", "port = 16384"]
            with open("config.txt", "w") as config:
                config.write("\n".join(options))

        #read the config file and store the configs in a dict
        self.configs = {"host": "", "port": ""}
        with open("config.txt", "r") as config:
            for line in config:
                line = line.strip("\n").split("=")
                option = line[0].strip().lower()
                value = line[1].strip()
                self.configs[option] = value if option != "port" else int(value)
        return self.configs

#run the server
if __name__ == "__main__":
    Server()