from server.server_handler import server_start, server_stop

if __name__ == '__main__':
    server_start()
    # when game stops, stop
    server_stop()
