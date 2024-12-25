import socket

STEP_TURTLE_PLAYER = 50

turtles = {
    'red': None,
    'blue': None,
    'yellow': None
}

players = {}

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('0.0.0.0', 12345))

start_pos = 100
finish_pos = 800

def parse_message(message):
    message_parse = message.decode('utf-8')
    message_parse = message_parse.split()
    return message_parse

def assign_turtle_player(addr):
    global turtles
    global players
    for key, value in turtles.items():
        if value is None:
            turtles[key] = addr
            players[addr] = start_pos
            return key
    return None

def move_turtle_player(addr):
    global players
    players[addr] += STEP_TURTLE_PLAYER

def send_all_player_game_status(socket, message=None):
    global players
    global turtles
    game_status = "GAME POS:\n"

    for color, player_addr in turtles.items():
        if player_addr is not None:
            game_status += f"{color} : {players[player_addr]}\n"

    if message:
        game_status += message + "\n"

    for player_addr in players:
        socket.sendto(game_status.encode('utf-8'), player_addr)

connected_players = 0

while True:
    message, addr = server.recvfrom(1024)

    message = parse_message(message)
    message_type = message[0]

    if message_type == "CONNECT":
        turtle_color = assign_turtle_player(addr)
        if turtle_color is not None:
            response = f"SELECT : {turtle_color}"
            server.sendto(response.encode('utf-8'), addr)
            connected_players += 1
            if connected_players == 2:
                send_all_player_game_status(server, "Два игрока подключились! Игра начинается.")
        else:
            response = "Все черепашки уже заняты. Подключение невозможно."
            server.sendto(response.encode('utf-8'), addr)
    elif message_type == "MOVE":
        if connected_players < 2:
            response = "Ожидание других игроков. Минимум 2 игрока для начала игры."
            server.sendto(response.encode('utf-8'), addr)
        elif addr in players:
            move_turtle_player(addr)
            send_all_player_game_status(server)