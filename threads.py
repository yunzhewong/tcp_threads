class SocketThreadController:
  def __init__(self): 
    self.handlers = []
    self.threads = []
    self.clients = []
  
  def add_thread(self, handler, thread, client):
    self.handlers.append(handler)
    self.threads.append(thread)
    if client is not None:
      self.clients.append(client)

  def stop(self):
    for client in self.clients:
      client.close()
    for handler in self.handlers:
      handler.close()
    for thread in self.threads:
      thread.join()

class ThreadHandler:
  def __init__(self):
    self.closed = False

  def is_closed(self):
    return self.closed;

  def close(self):
    self.closed = True
