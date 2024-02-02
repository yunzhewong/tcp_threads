import socket
import time
import threads
import threading

def send_to_server(value, client_socket, threadHandler):
  try:
    while not threadHandler.is_closed():
      message = f"{value}"
      client_socket.send(message.encode())

      response = client_socket.recv(4096)
      if not response:
        print("No Response, closing")
        client_socket.close()
        break
      
      data = response.decode()
      print(f"Data received: {data}")
      time.sleep(1)
  except:
    print("Thread error")
  client_socket.close()

def start_client():
  
  host = socket.gethostname()
  port = 8080

  controller = threads.SocketThreadController()

  for i in range(10):
    print(f"Client {i} created")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    threadHandler = threads.ThreadHandler()
    upload_thread = threading.Thread(target=send_to_server, args=(i, client_socket,threadHandler,))
    upload_thread.start()
    controller.add_thread(threadHandler, upload_thread, client_socket)

  try:
    while True:
      pass
  except KeyboardInterrupt:
    controller.stop()
    print("Client stopped")
  

if __name__ == "__main__":
  start_client()