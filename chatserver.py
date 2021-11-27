import threading
import socket
host = '127.0.0.1'
port = 65534
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

clients = []
names = []


def broadcast(message, name):
    temp = message.decode('utf-8')
    if ':' in temp:
        temp = temp.split(':')[1][1:]
    for client in clients:
        if (clients.index(client) != names.index(name)) and (len(temp) != 1) and (len(message)!=0):
            client.send(message)

def personal(client, name, sec_user):
    while True:
        try:
            message = client.recv(1024)
            temp = message.decode('utf-8')
            if ':' in temp:
                temp = temp.split(':')[1][1:]

            if temp=='q':
                index = clients.index(client)
                clients.remove(client)
                client.close()
                name = names[index]
                broadcast(f'{name} has left the chat room!'.encode('utf-8'), name)
                names.remove(name)
                break

            elif temp=='l':
                client.send(f">>> {len(names)} users are currently active".encode('utf-8'))
                lis = ", ".join(names)
                client.send(f"\n>>> {lis}".encode('utf-8'))

            elif temp=='h':
                client.send("\n####\n\n  'l' - list all active users\n  'c' - Connect to a single user\n  'r' - Return to chat room\n  'q' - Exit chat room\n\n####\n".encode('utf-8'))            
            
            elif temp=="c":
                client.send('>>> Connecting to single user... \n>>> Enter username : '.encode('utf-8'))
                sec_user = client.recv(1024).decode('utf-8').split(':')[1][1:]

                if sec_user not in names:
                    client.send(">>> User doesn't exist or is inactive ".encode('utf-8'))
                    continue

                personal(client, name, sec_user)
                break

            elif temp=='r':
                client.send(">>> Returning back to chat room ".encode('utf-8'))
                handle_client(client, name)
                break

            sec_cli = clients[names.index(sec_user)]

            pers_m = message.decode('utf-8').split(':')
            pers_m[0] = pers_m[0]+"(Personal) "
            pers_m = ":".join(pers_m)

            sec_cli.send(pers_m.encode('utf-8'))
                

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast(f'{name} has left the chat room!'.encode('utf-8'))
            names.remove(name)
            break

# Function to handle clients'connections
def handle_client(client, name):
    while True:
        try:
            message = client.recv(1024)
            temp = message.decode('utf-8')
            if ':' in temp:
                temp = temp.split(':')[1][1:]


            if temp=='q':
                print(">>>",name,"left the chat room")
                index = clients.index(client)
                clients.remove(client)
                client.close()
                name = names[index]
                broadcast(f'{name} has left the chat room!'.encode('utf-8'), name)
                names.remove(name)
                break

            elif temp=='l':
                client.send(f">>> {len(names)} users are currently active".encode('utf-8'))
                lis = ", ".join(names)
                client.send(f">>> {lis}".encode('utf-8'))

            elif temp=='h':
                client.send("\n####\n\n  'l' - list all active users\n  'c' - Connect to a single user\n  'r' - Return to chat room\n  'q' - Exit chat room\n\n####\n".encode('utf-8'))
            
            elif temp=="c":
                client.send('>>> Connecting to single user... \n>>> Enter username : '.encode('utf-8'))
                sec_user = client.recv(1024).decode('utf-8').split(':')[1][1:]

                if sec_user not in names:
                    client.send(">>> User is inactive ".encode('utf-8'))
                    continue

                personal(client, name, sec_user)
                break

            elif temp=='r':
                client.send(">>> Returning back to chat room ".encode('utf-8'))
                handle_client(client, name)
                break
                

            broadcast(message, name)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast(f'{name} has left the chat room!'.encode('utf-8'))
            names.remove(name)
            break


# Main function to receive the clients connection
def receive():
    print('>>> Server started ...')
    while True:
        print('>>> Server is running and listening ...')
        client, address = server.accept()
        
        client.send('username'.encode('utf-8'))
        name = client.recv(1024).decode('utf-8')
        names.append(name)
        clients.append(client)

        print(f'>>> Connection is established with {name} {str(address)}')

        broadcast(f'** {name} has connected to the chat room **'.encode('utf-8'), name)
        client.send('\n** You are now connected to chat room! **'.encode('utf-8'))
        client.send("\n####\n\n  'l' - list all active users\n  'c' - Connect to a single user\n  'r' - Return to chat room\n  'q' - Exit chat room\n  'h' - help\n\n####\n".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,name))
        thread.start()


if __name__ == "__main__":
    receive()