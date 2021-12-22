import socket
from sys import argv
#Socket programming project for tic tac toe
# Mohammad Andalibi & Mohammadmahdi Mohammadi – summer 2020

#client_side

# Socket programming is a way of connecting two nodes on a network to communicate with each other.
# One socket(node) listens on a particular port at an IP, while other socket reaches out to the other
# to form a connection. Server forms the listener socket while client reaches out to the server.
# They are the real backbones behind web browsing. In simpler terms there is a server and a client.

class Client():

    #Error Message - Cannot Connect To Server / Network -
    # Unable To Reach Server / Network. Root Cause - The issue can be caused by
    # Carrier Data not available or Data connection is slow causing the app to timeout.
    # Fix - The phone needs to be checked for various settings within app & device

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        port_number = input("Please enter the port:");
        turn = True
        while turn:
            try:
                print("Connecting to the game server...");
                self.client_socket.connect(('127.0.0.1', int(port_number)));
                turn = False;
                print("Connected to the game server...");
            except:
                print("There is an error when trying to connect to " + '127.0.0.1' + "::" + str(port_number));
                self.__connect_failed__()
        try:
            # point your browser at https://ping.pe and the website will display your
            # current IP address and location. Enter that IP address in the 'Ping' box
            # at the top of the page, and click 'Go'

            self.player_id = int(self.received(128, "A"));
            self.send("c", "1");
            msg = self.client_socket.recv(2).decode();

            if(msg[0]=="G"):
                g = input("enter number of grid: ")
                self.send("G", g);
            if(msg[0]=="T"):
                are_you_play = input("do you play ? [1]Yes  or [0]No")
                self.send("T", are_you_play);
            msg = self.client_socket.recv(2).decode();
            self.gridOfGame = int(msg[1])

            print("Welcome to Tic Tac  player " + str(
                self.player_id) + "\nPlease wait for another player to join the game...")
            self.role = str(self.received(2, "R"));


            self.send("c", "2");
            self.match_id = int(self.received(128, "I"));
            self.send("c", "3");
            print(("You are now matched with player " + str(self.match_id) + "\nYou are the \"" + self.role + "\""));
            self.__main_loop();
        except:
            print(("Game finished !"));

        self.client_socket.shutdown(socket.SHUT_RDWR);
        self.client_socket.close();

    # Players install a "client" for the game on their computer and then connect to the game
    # servers via an internet connection. ... If a server fails, players can still enter the
    # game through the other servers. After having checked the data of a player, the client is connected to the game server.

    def __connect_failed__(self):
        choice = input("1.change address and port(1) or 2.retry(2)?");
        if (choice == "1"):
            address = input("Please enter the address:");
            port_number = input("Please enter the port:");

    def send(self, command_type, msg):
        print("send: (", command_type, ") ", msg)
        try:
            self.client_socket.send((command_type + msg).encode());
        except:
            self.__connection_lost();

    def received(self, size, expected_type):

        try:
            print("size",size)
            msg = self.client_socket.recv(size).decode();
            print("recived", msg)

            if(msg[0] == "B"):
                return msg[1:];
            if (msg[0] == "Q"):
                why_quit = "";
                try:
                    why_quit = self.client_socket.recv(1024).decode();
                except:
                    pass;
                print(msg[1:] + why_quit);
                raise Exception;

        # It doesn’t send any data. It doesn’t receive any data. It just produces “client” sockets.
            # Each clientsocket is created in response to some other “client” socket doing a connect()
            # to the host and port we’re bound to. As soon as we’ve created that clientsocket, we go back
            # to listening for more connections. The two “clients” are free to chat it up - they are using
            # some dynamically allocated port which will be recycled when the conversation ends.

            elif (msg[0] != expected_type):
                print("The received command type \"" + msg[
                    0] + "\" does not " + "match the expected type \"" + expected_type + "\".");

                self.__connection_lost();

            elif (msg[0] == "I"):
                print("msg: ",msg[1:])
                return int(msg[1:]);
            else:
                return msg[1:];

            return msg;
        except:
            self.__connection_lost();
        return None;

    def __connection_lost(self):
        print("connection lost.");
        try:
            self.client_socket.send("q".encode());
        except:
            pass;
        raise Exception;

    #A server can just as well be a gaming machine as a gaming machine
    # can be a server. Alltough the hardware in the server is mostly oriented
    # at raw data processing and no graphics, adding a graphics card will solve that problem

    def __main_loop(self):
        while True:

            temp_number = self.gridOfGame*self.gridOfGame*2

            temp = self.received(temp_number+1, "B");
            board_content = temp[1:]
            command = self.received(2, "C");

             #When the connect completes, the socket s can be used to send in a request for
            # the text of the page. The same socket will read the reply, and then be destroyed.
            # That’s right, destroyed. Client sockets are normally only used for one exchange
            # (or a small set of sequential exchanges)

            if (command == "Y"):

                self.move(board_content,temp_number);
            elif (command == "N"):
                self.player_wait();

                move = self.received(3, "I");
                print("Your opponent took up number " , move);

            elif (command == "D"):
                print("It's a draw.");
                break;
            elif (command == "W"):

                print("You WIN!");

                self.__draw_winning_path__(self.received(4, "P"));

                break;
            elif (command == "L"):

                print("You lose.");

                self.__draw_winning_path__(self.received(4, "P"));

            #A couple things to notice: we used socket.gethostname() so that the socket would
                # be visible to the outside world. If we had used s.bind(('localhost', 80)) or
                # s.bind(('127.0.0.1', 80)) we would still have a “server” socket, but one that
                # was only visible within the same machine. s.bind(('', 80)) specifies that the
                # socket is reachable by any address the machine happens to have.

                break;
            else:

                print("Error: unknown message was sent from the server");
                break;


    def move(self, board_string,temp_number):
        while True:
            try:

                mm = input("Please enter the position 1 to ...: ");
                position = int(mm)
            except:
                print("Invalid input.");
                continue;

            if (position >= 1 and position <= len(board_string)/2 ):

                if (board_string[position*2 ] != " "):

                    print("That position has already been taken." + "Please choose another one.");
                else:

                    break;
            else:
                print("Please enter a value between 1 and ", len(board_string)/2 ," that" + "corresponds to the position on the grid board.");


        #pconfig. Ipconfig is a Console Command which can be issued to the Command Line Interpreter
        # (or command prompt) to display the network settings currently assigned to any or all network
        # adapters in the machine

        if(position<10):
            temp = "0"+ str(position)
        else:
            temp = str(position)
        self.send("i", temp);

    def player_wait(self):
        print("Waiting for the other player to make a move...");



    def __draw_winning_path__(self, winning_path):
        readable_path = "";
        for c in winning_path:
            readable_path += str(int(c) + 1) + ", "

        print("The path is: " + readable_path[:-2]);

    def show_board_pos(s):

    #There’s actually 3 general ways in which this loop could work - dispatching a thread to handle clientsocket,
    # create a new process to handle clientsocket, or restructure this app to use non-blocking sockets, and multiplex
    # between our “server” socket and any active clientsockets using select. More about that later. The important thing
    # to understand now is this: this is all a “server” socket does.

        new_s = list("123456789");
        for i in range(0, self.gridOfGame*self.gridOfGame):
            if (s[i] != "9"):
                new_s[i] = s[i];
        return "".join(new_s);

    def format_board(s):


        print("|" + s[0] + "|" + s[1] + "|" + s[2] + "|\n"
                + "|" + s[3] + "|" + s[4] + "|" + s[5] + "|\n"
                + "|" + s[6] + "|" + s[7] + "|" + s[8] + "|\n");


def main():
    _client = Client();

    #Probably the worst thing about using blocking sockets is what happens when the other
    # side comes down hard (without doing a close). Your socket is likely to hang. SOCKSTREAM
    # is a reliable protocol, and it will wait a long, long time before giving up on a connection.
    # If you’re using threads, the entire thread is essentially dead. There’s not much you can do about it.
    # As long as you aren’t doing something dumb, like holding a lock while doing a blocking read, the thread
    # isn’t really consuming much in the way of resources. Do not try to kill the thread - part of the reason
    # that threads are more efficient than processes is that they avoid the overhead associated with the automatic recycling
    # of resources. In other words, if you do manage to kill the thread, your whole process is likely to be screwed up.


if __name__ == "__main__":
    main();