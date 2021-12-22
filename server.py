import socket
import threading
import time

#Socket programming project for tic tac toe
# Mohammad Andalibi & Mohammadmahdi Mohammadi – summer 2020

#server_side

#The term network programming refers to writing programs that
# execute across multiple devices (computers), in which the devices
# are all connected to each other using a network.


# Python time method ctime() converts a time expressed in seconds
# since the epoch to a string representing local time. If secs is
# not provided or None, the current time as returned by time() is used.
# This function is equivalent to asctime(localtime(secs)). Locale information is not used by ctime().

t = time.ctime(time.time())
now = time.localtime()
file_name = "test2.txt"
file = open(file_name, "w")
from sys import argv
import logging
logging.basicConfig(level=logging.DEBUG,
	format='[%(asctime)s] %(levelname)s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S',filename='ttt_server.log');

console = logging.StreamHandler();
console.setLevel(logging.INFO);
logging.getLogger('').addHandler(console);

#Sockets provide the communication mechanism between two computers using TCP.
# A client program creates a socket on its end of the communication and attempts
# to connect that socket to a server.


#When the connection is made, the server creates a socket object on its end of the communication.
# #The client and the server can now communicate by writing to and reading from the socket.
#The java.net.Socket class represents a socket, and the java.net.ServerSocket class provides a mechanism for
# the server program to listen for clients and establish connections with them.

class Server():
    def __init__(self):
            port = input("Please enter the port:");
            """Initializes the server game object."""
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            while True:
                try:
                    self.server_socket.bind(('127.0.0.1', int(port)));
                    logging.info("Reserved port " + str(port));
                    self.server_socket.listen(1);
                    logging.info("Listening to port " + str(port));
                    break;
                except:
                    # Caught an error
                    logging.warning("There is an error when trying to bind " + str(port))
                    choice = input("[A]bort, [C]hange port, or [R]etry?")
                    if (choice.lower() == "a"):
                        exit();
                    elif (choice.lower() == "c"):
                        port_number = input("Please enter the port:");
            self.start();

    def close(self):
        self.server_socket.close()

    def start(self):
        self.Connected_player = [];
        self.lock_matching = threading.Lock();
        self.mainboard();

    def mainboard(self):
        # the low-level communication details, allowing you to write programs that focus on solving the problem at hand.
        while True:
            id, client_address = self.server_socket.accept();

            new_player = Player(id);

            self.Connected_player.append(new_player);
            try:

                threading.Thread(target=self.__client_thread, args=(new_player,)).start()
            except:
                logging.error("Failed to create thread.");

    #After the connections are established, communication can occur using I/O streams.
    # Each socket has both an OutputStream and an InputStream. The client's OutputStream
    # is connected to the server's InputStream, and the client's InputStream is connected
    # to the server's OutputStream.


    def __client_thread(self, player):
        try:
            player.send("A", str(player.id));
            if (player.recv(2, "c") != "1"):
                # An error happened
                logging.warning("Client " + str(player.id) + " didn't confirm the initial message.")
                return;
            do_you_play = True
            print(str(player.id))

            while player.is_waiting :

                match_result = self.matching_player(player);

                do_you_play = True
                if (match_result is None):
                    time.sleep(1);

                else:

    #If the ServerSocket constructor does not throw an exception,
    # it means that your application has successfully bound to the
    # specified port and is ready for client requests.

                    player.send("T", "T")
                    _bool = player.recv(2, "T")
                    if (_bool == "0"):
                        do_you_play = False
                        player.is_waiting = False
                        match_result.is_waiting = True

                    if(do_you_play):
                        match_result.send("G", "G")
                        _grid = match_result.recv(2, "G")
                        player.send("X",str(_grid))
                        match_result.send("X",str(_grid))
                        new_game = Game();
                        new_game.grid =int(_grid);
                        new_game.player1 = player;
                        new_game.player2 = match_result;
                        # Create an empty string for empty board content
                        new_game.board_content = "";
                        m = int(_grid)*int(_grid)
                        for i in range (1,m):
                            new_game.board_content += "  "
                        print("=",new_game.board_content,"=")
                        try:
                             new_game.start();
                        except:
                            logging.warning("game between " + str(new_game.player1.id) + " and " + str(
                                new_game.player2.id) + " is finished unexpectedly.");
                    return;
        except:
            print("Player " + str(player.id) + " disconnected.");
        finally:

            if(player.is_waiting==False):
               self.Connected_player.remove(player);

    def matching_player(self, player):

        self.lock_matching.acquire();
        try:
            print()
            for member in self.Connected_player:

                if (member.is_waiting and member is not player):

                    player.match = member;
                    member.match = player;

                    player.role = "X";
                    member.role = "O";

                    player.is_waiting = False;
                    member.is_waiting = False;

                    return member;
        finally:
            self.lock_matching.release();
        return None;

    #Basically the system involves the user creating one or more logger
    # objects on which methods are called to log debugging notes, general
    # information, warnings, errors etc. Different logging 'levels' can be
    # used to distinguish important messages from less important ones.

class Player:
    count = 0;

    def __init__(self, connection):

        Player.count = Player.count + 1
        self.id = Player.count;
        self.connection = connection;
        self.is_waiting = True;

    def send(self, command_type, msg):

      file.write(t)
      file.write(" \t","send: (",command_type,")", msg,"-","\n")
      self.connection.send((command_type + msg).encode());

    def recv(self, size, expected_type):

        try:
            msg = self.connection.recv(size).decode();
            file.write(t)
            file.write(" \t","recived: ",msg,"-",expected_type,"\n")

            __string_list = list(msg)

            if (__string_list[0] == "q"):
               # logging.info(msg[1:]);
                self.__connection_lost();
            elif(__string_list[0]=="G"):
                __new_string = "".join(__string_list[1:])
                return __new_string;
            elif (__string_list[0] == "T"):
                __new_string = "".join(__string_list[1:])
                return __new_string;
        #The APIs are structured so that calls on the Logger APIs can be cheap
            # when logging is disabled. If logging is disabled for a given log level,
            # then the Logger can make a cheap comparison test and return. If logging
            # is enabled for a given log level, the Logger is still careful to minimize
            # costs before passing the LogRecord into the Handlers. In particular, localization
            # and formatting (which are relatively expensive) are deferred until the Handler requests them.

            elif (__string_list[0] != expected_type):
                self.__connection_lost();
            elif (__string_list[0] == "i"):
                __new_string = "".join(__string_list[1:])
                return __new_string;
            # In other case
            else:
                __new_string = "".join(__string_list[1:])
                return __new_string;
            __new_string = "".join(__string_list)
            return __new_string;
        except:
            self.__connection_lost();
        return None;

    # TCP − TCP stands for Transmission Control Protocol, which allows
    # for reliable communication between two applications. TCP is typically
    # used over the Internet Protocol, which is referred to as TCP/IP.

    def check_connection(self):
        self.send("E", "z");
        if (self.recv(2, "e") != "z"):
            self.__connection_lost();

    def send_match_info(self):
        self.send("R", self.role);
        if (self.recv(2, "c") != "2"):
            self.__connection_lost();
        self.send("I", str(self.match.id));
        if (self.recv(2, "c") != "3"):
            self.__connection_lost();

    def __connection_lost(self):

        try:
            self.match.send("Q", "The other player has lost connection" + " with the server.\nGame over.")
        except:
            pass;

        raise Exception;


class Game:
    grid = 0;

    def start(self):
        self.player1.send_match_info();
        self.player2.send_match_info();


        while True:
            # Player 1 move
            if (self.move(self.player1, self.player2)):
                return;
            # Player 2 move

            if (self.move(self.player2, self.player1)):
                return;

    def move(self, moving_player, waiting_player):
        moving_player.send("B", ("".join(self.board_content)));
        waiting_player.send("B",("".join(self.board_content)));

        moving_player.send("C", "Y");
        waiting_player.send("C", "N");

        _move = moving_player.recv(3, "i");

        waiting_player.send("I", _move);

        _string_list = list(_move)
        if (int(_string_list[1]) == 0):
            _new_string = int(_string_list[2])
        else:
            _new_string = "".join(_string_list[1:])
        __move = int(_new_string)

        if (self.board_content[(__move-1)*2] == " "):
            string_list = list(self.board_content)

            string_list[(__move-1)*2] = moving_player.role;
            string_list[(__move-1)*2+1] = moving_player.role;
            new_string = "".join(string_list)
            self.board_content =  new_string
        result = -1
        result = self.check_winner(moving_player);
       # print("Result: ",result)
        if (result >= 0):

            moving_player.send("C", "W");
            waiting_player.send("B","L");

#chevron_right.
# Import socket module. import socket.
# Create a socket object. s = socket.socket()
# Define the port on which you want to connect. port = 12345.
# connect to the server on local computer. s.connect(( '127.0.0.1' , port))
# receive data from the server. print s.recv( 1024 ) # close the connection. ...
#chevron_right.

            return False;

    def check_winner(self, _player):

        for i in range(0,self.grid*self.grid,self.grid):
                if(self.board_content[1+i]==self.board_content[3+i]==self.board_content[5+i]==self.board_content[7+i]):
                    if(_player.role ==self.board_content[1+i]):
                        return 1,
                if (self.board_content[1 + i] == self.board_content[5 + i] == self.board_content[9 + i] ==self.board_content[13 + i] ):
                    if (_player.role == self.board_content[1 + i]):
                        return 1,
        if (self.board_content[1 ] == self.board_content[6] == self.board_content[11] == self.board_content[16]):
            if (_player.role == self.board_content[1]):
                return 1,
        if (self.board_content[4] == self.board_content[7] == self.board_content[10] == self.board_content[13]):
            if (_player.role == self.board_content[4]):
                return 1,

        return -1

def main():
    try:
        _server = Server()

    except BaseException as e:
        logging.critical("Server critical failure.\n" + str(e));


if __name__ == "__main__":
    # If this script is running as a standalone program,
    # start the main program.
    main();





