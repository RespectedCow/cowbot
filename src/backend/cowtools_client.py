# Imports
import socket
import time

# Set up some variables
others_path = "../../data/others"

# Functions
def retractor(num):
    alphabets = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    index = 0
    for i in range(0, num):
        index += 1
        if index > (len(alphabets) - 1):
            index = 0

    return index

def decryptPass(host, num):
    decrypted_token = ""
    alphabets = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    # Search for encrypted token
    with open('{}/clienttoken.txt'.format(others_path), "r") as f:
        for line in f:
            line = line.strip().split()

            if line[0] == host:
                print("Client token found!")
                print("Beginning decryption process")
                # Beginning decryption process
                for char in line[1]:
                    if char.isalpha():
                        if char.islower(): # Deal with upper and lowercase
                            decrypted_token = decrypted_token + alphabets[(alphabets.index(char.lower()) - (1 * num))]
                        else:
                            decrypted_token = decrypted_token + alphabets[(alphabets.index(char.lower()) - (1 * num))].upper()
                    elif char.isdigit():
                        decrypted_token += char

    time.sleep(1)
    return decrypted_token

def encrypt(servertoken, host, num):
    
    # vars
    alphabets = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    # Check if token for host exist
    with open("{}/clienttoken.txt".format(others_path), "r") as f:
        for line in f:
            line = line.strip().split()
            
            if len(line) == 2:
                if line[0] == host:
                    print("Token for host exists!")
                    print("Exiting!")

                    return "exist!"

    # Messages
    print("Server token is " + servertoken) # Messages
    print("Creating token for " + host)

    token = ""

    # Create token
    for char in servertoken:
        # Create the token
        # get char type
        if char.isalpha():
            if char.islower(): # Deal with upper and lowercase
                token += alphabets[retractor(alphabets.index(char.lower()) + (1 * num))]
            else:
                token += alphabets[retractor(alphabets.index(char.lower()) + (1 * num))].upper()
        elif char.isdigit():
            token += char

    # Start encryption
    encrypted_token = ""

    for char in token:
        # We are gonna use ceasar's cipher with the random number as a multiplier
        # get char type
        if char.isalpha():
            if char.islower(): # Deal with upper and lowercase
                encrypted_token += alphabets[retractor(alphabets.index(char.lower()) + (1 * num))]
            else:
                encrypted_token += alphabets[retractor(alphabets.index(char.lower()) + (1 * num))].upper()
        elif char.isdigit():
            encrypted_token += char

    # Write the token to clienttoken.txt
    clienttokentxt = open('{}/clienttoken.txt'.format(others_path), "w+")
    clienttokentxt.write(host + " " + encrypted_token + "\n")

    clienttokentxt.close()

    return token

# Client class
class Client:
    def __init__(self, server):
        # Connect to server
        # Set up variables and token
        self.server = server
        port = 2000        # Default cowtools port
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.server, port))
        endit = False

        # give connection type
        client.send("token business".encode("utf-8"))

        # get decryption key
        decryption_key = str(client.recv(1026).decode("utf8"))

        if decryption_key == "token exist!":
            print("Server has another client token! Delete it from server end!")

        data = client.recv(1026)
        strings = str(data, 'utf8')
        num = int(strings)

        token = encrypt(decryption_key, self.server, num)
        if token == "exist!":
            client.send("exist!".encode("utf8"))

            time.sleep(0.1)
            endit = True

        if endit == False:
            print("Put this when the server requests it(In server console): " + token)

            client.send("created token".encode('utf8'))

            while True:
                data = client.recv(1026)
                if not data:
                    break
                # convert data to string
                message = data.decode("utf8")
                print(message)

                print("Session closed.")

        # Store token in temporary memory
        self.token = token

    def get_server_wan_ip(self):
        # Connect to server
        # Set up variables
        port = 2000        # Default cowtools port
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, port))

        # Give connection type
        client.send("command issue".encode("utf8"))
                    
        # get decryption key
        decryption_key = str(client.recv(1026).decode("utf8"))

        if decryption_key == "token exist!":
            print("Server has another client token! Delete it from server end!")

        data = client.recv(1026)
        strings = str(data, 'utf8')
        num = int(strings)

        client.send(self.token.encode("utf8"))
        time.sleep(0.2)
        client.send("cowtools get ip".encode("utf8")) # Test command