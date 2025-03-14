from random import random
from math import sqrt, cos, log, pi

def gen_exponential_time(rate: float):
  return -log(random()) / rate

def gen_normal_time(mean: float, std_dev: float):
  while True:
    u1 = random()
    u2 = random()
    z = sqrt(-2.0 * log(u1)) * cos(2.0 * pi * u2)
    if mean + std_dev * z > 0:
      return mean + std_dev * z

class QueueSimulator:
  # Arrival process is exponential with rate lambda_rate

  def __init__(self, lambda_rate: float, gen_service_time: callable, gen_service_args: tuple, num_servers: int, max_users: int, population_size: int, simulation_time: float):
    self.lambda_rate = lambda_rate
    self.gen_service_time = gen_service_time
    self.gen_service_args = gen_service_args
    self.num_servers = num_servers
    self.max_users = max_users
    self.population_size = population_size
    self.time = 0
    self.queue: list[float] = []
    self.next_arrival = gen_exponential_time(lambda_rate)
    self.next_departures: list[float] = [float('inf')]
    self.servers_busy = 0
    self.simulation_time = simulation_time
    self.file = open("output.txt", "w")

    self.total_entries = 0
    self.total_service_users = 0.0
    self.total_queue_users = 0.0
    self.total_queue_time = 0.0
    self.total_service_time = 0.0

    self.simulate()
    self.file.close()

  def simulate(self):
    while self.time < self.simulation_time:
      if self.next_arrival < self.next_departures[0]:
        # Arrival event
        self.total_service_users += self.servers_busy * (self.next_arrival - self.time)
        self.total_queue_users += len(self.queue) * (self.next_arrival - self.time)

        self.time = self.next_arrival

        if len(self.queue) + self.servers_busy == self.max_users or self.population_size == 0:
          self.file.write(f"Usuario rejeitado em {self.time:.5f}\n")
          self.next_arrival = self.time + gen_exponential_time(self.lambda_rate)
          continue

        self.file.write(f"Usuario chega em {self.time:.5f}\n")
        self.population_size -= 1
        self.total_entries += 1
        if self.servers_busy < self.num_servers:
          self.file.write(f"Usuario entra em servico em {self.time:.5f}\n")
          self.servers_busy += 1
          service_time = self.gen_service_time(*self.gen_service_args)
          self.total_service_time += service_time
          self.insert_departure(self.time + service_time)
        else:
          self.queue.append(self.time)
        self.next_arrival = self.time + gen_exponential_time(self.lambda_rate)
      else:
        # Departure event
        next_departure = self.next_departures.pop(0)
        self.total_service_users += self.servers_busy * (next_departure - self.time)
        self.total_queue_users += len(self.queue) * (next_departure - self.time)

        self.time = next_departure
        self.file.write(f"Usuario sai em {self.time:.5f}\n")
        self.population_size += 1
        if self.queue:
          self.file.write(f"Usuario entra em servico em {self.time:.5f}\n")
          arrival_time = self.queue.pop(0)
          self.total_queue_time += self.time - arrival_time
          service_time = self.gen_service_time(*self.gen_service_args)
          self.total_service_time += service_time
          self.insert_departure(self.time + service_time)
        else:
          self.servers_busy -= 1
    
    self.print_results()
  
  def insert_departure(self, dep: float):
    for i, departure_time in enumerate(self.next_departures):
      if dep < departure_time:
        self.next_departures.insert(i, dep)
        break

  def avg_queue_time(self):
    return self.total_queue_time / self.total_entries
  
  def avg_service_time(self):
    return self.total_service_time / self.total_entries
  
  def avg_system_time(self):
    return self.avg_queue_time() + self.avg_service_time()
  
  def avg_queue_users(self):
    return self.total_queue_users / self.time
  
  def avg_service_users(self):
    return self.total_service_users / self.time
  
  def avg_system_users(self):
    return self.avg_queue_users() + self.avg_service_users()
  
  def print_results(self):
    print("\nResultados da simulação")
    print("> Tempo médio na fila:", self.avg_queue_time())
    print("> Tempo médio em serviço:", self.avg_service_time())
    print("> Tempo médio no sistema:", self.avg_system_time())
    print("> Número médio de usuários na fila:", self.avg_queue_users())
    print("> Número médio de usuários em serviço:", self.avg_service_users())
    print("> Número médio de usuários no sistema:", self.avg_system_users())
  
