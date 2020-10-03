import socket
from _thread import *
from game import Game
import pickle

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER = "10.0.0.133"
PORT = 5000
try:
    sock.bind((SERVER, PORT))
except socket.error as e:
    print(e)

sock.listen(100)
print("Waiting for connection. Server started.")

games = {}
idCount = 0


def threaded_client(connection, player, game_num):
    global idCount
    connection.sendall(str.encode(str(player)))

    while True:
        try:
            data = connection.recv(4028).decode()
            data = data.split(",")

            if player == 0:
                games[game_num].player_one_name = data[0]
            else:
                games[game_num].player_two_name = data[0]

            if game_num in games:
                if not data:
                    break
                else:
                    if data[1] == "mate":
                        games[game_num].update_loser(player)
                    elif data[1] != "get":
                        games[game_num].update_move(player, data[1:5])
                    connection.sendall(pickle.dumps(games[game_num]))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[game_num]
    except:
        pass
    idCount -= 1
    connection.close()


while True:
    conn, addr = sock.accept()

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
