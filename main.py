import socket
import threads
import time
import threading

lock = threading.Lock()

def show_data(data, threadHandler):
  while not threadHandler.is_closed():
    with lock:
      print(data)
    time.sleep(1)

def handle_client(data, client_socket, threadHandler):
  try: 
    while True:
      if (threadHandler.is_closed()):
        print("Thread stopped")
        client_socket.close()
        break

      received = client_socket.recv(4096)

      if not received:
        print("No data found")
        client_socket.close()
        break

      message = int(received.decode())
      with lock:
        data[message] = message

      response = f"Messaged Received {message}"
      
      client_socket.send(response.encode())
  except Exception as e:
    print(e)
    print("Thread Error Caught")


def start_server(): 
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  host = socket.gethostname()
  port = 8080

  print(f"Listening on {host}: {port}")
  server_socket.bind((host, port))

  server_socket.listen(5)

  controller = threads.SocketThreadController()
  
  data = [0 for i in range(10)]
  threadHandler = threads.ThreadHandler()
  data_thread = threading.Thread(target=show_data, args=(data, threadHandler))
  data_thread.start()
  controller.add_thread(threadHandler, data_thread, None)
  try:
    while True:
      client_socket, addr = server_socket.accept()
      print(f"Got connection from {addr}")
      threadHandler = threads.ThreadHandler()
      client_thread = threading.Thread(target=handle_client, args=(data, client_socket,threadHandler,))
      client_thread.start()
      controller.add_thread(threadHandler, client_thread, client_socket)
  except KeyboardInterrupt:
    controller.stop()
    print("Server stopped")

if __name__ == "__main__":
  start_server()

