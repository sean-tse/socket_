import socket
import threading
import time

HEADER = 64 # first message length
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "||DISCONNECT||"
END_INPUT = "||END||"
SHUTDOWN = "||||||"
SERVER = "192.168.1.107"
ADDR = (SERVER, PORT)

stop_threads = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # connection Family (internet), type of connection
client.connect(ADDR)

# Sends a message to the server
def send(msg):
    message = msg.encode(FORMAT) # the content we want to send
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT) # the first msg we send to prepare server
    send_length += b' ' * (HEADER - len(send_length)) # pads until the proper length
    
    client.send(send_length)
    client.send(message)

# receives a single message from the server
def receive_one(): 
    try:
        msg_length = client.recv(HEADER).decode(FORMAT) # 
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
            return msg
        return None
    except:
        pass

# Asks for a single input and sends it
def send_singular_input():
    global stop_threads
    msg = input("\nInput: \n")
    if msg == END_INPUT:
        stop_threads = True
        return 
    if msg == DISCONNECT_MESSAGE or msg == SHUTDOWN:
        stop_threads = True
        send(msg)
        exit(0)
        return
    
    send(msg)
    time.sleep(0.1)



# Continuously awaits user input and sends it to server
def send_inputs():
    while True and not stop_threads:
       send_singular_input()

# Receives communication from server
def receive_all():
    while True and not stop_threads:
        msg = receive_one()
        if msg:
            handle_msg(msg)

def handle_msg(msg):
    # handles content of message
    print(f"|Message Received| {msg} from SERVER")
    send_singular_input()


def main():
    global stop_threads
    try:
        print("Client START")
        threading.Thread(target=receive_all).start()
        #send_singular_input() # First input
        while not stop_threads:
            pass
        send(DISCONNECT_MESSAGE)
        print("Disconnected")
    except:
        exit()
    
        

main()

