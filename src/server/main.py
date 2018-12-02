import socket
import sys
import pickle
import json
from _thread import *

HOST = ''	# all available interfaces
PORT = 4200	# Arbitrary non-privileged port
GAME_DATA = "../gamedata/config.json"

'''
"player_state": {
			"tester2": {
				"character": "wizard",
				"team": "red",
				"max_hp": 500,
				"cur_hp": 200,
				"max_energy": 100,
				"cur_energy": 100,
				"cooldowns": [0,0,10,0],
				"loc_x": 0,
				"loc_y": 0
			}
		},
        '''
        
class GameState:
    def __init__(self):
        self.characters = None
        self.abilities = None
        self.players = None
        self.objects = None
        
        self.load_data()
    
    def load_data(self):
        with open(GAME_DATA) as f:
            data = json.load(f)
        self.characters = data["characters"]
        self.abilities = data["abilities"]
        self.players = None
        self.objects = data["game_state"]["object_state"]
        
    def payload(self):
        payl = {
            "objects" : self.objects,
            "players" : self.players
        }
        return pickle.dumps(payl)


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    print("Socket Bound")

    s.listen(10)
    print("Socket Listening")
    
    return s

#handling connections. used to create threads
def clientthread(conn, game_state):
    conn.send(b'Welcome to the server. Type something and hit enter\n') #send only takes string
    try:
        while True:
            data = conn.recv(1024)
            reply = 'OK...' + data
            if not data: 
                break
        
            conn.sendall(reply)
            
    except KeyboardInterrupt:
        #came out of loop
        conn.close()

def serve(s, game_state):
    #now keep talking with the client
    try:
        while 1:
            #wait to accept a connection - blocking call
            conn, addr = s.accept()
            print ('Connected with ' + addr[0] + ':' + str(addr[1]))
            
            #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            start_new_thread(clientthread ,(conn, game_state))
    except KeyboardInterrupt:
        s.close()
    s.close()

if __name__ == "__main__":
    game_state = GameState()
    print("Game State Loaded.")
    
    server = start_server()
    serve(server, game_state)
    