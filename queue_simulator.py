from random import random
from math import sqrt, cos, log, pi

def gen_exponential_time(rate: float):
  if (rate == 0.0):
    return float('inf')
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
    self.simulation_time = simulation_time
    self.time = 0.0
    self.queue: list[float] = []
    self.next_arrival = gen_exponential_time(self.lambda_n())
    self.next_departures: list[float] = [float('inf')]
    self.servers_busy = 0
    self.file = open('output.txt', 'w', encoding='utf-8')
    self.last_arrival = 0.0
    # Variables for statistics
    self.total_entries = 0
    self.total_service_users = 0.0
    self.total_queue_users = 0.0
    self.total_queue_time = 0.0
    self.arrival_differences: list[float] = []
    self.service_times: list[float] = []

  def __del__(self):
    self.file.close()

  def simulate(self):
    while self.time < self.simulation_time:
      if self.next_arrival < self.next_departures[0]:
        self.handle_arrival()
      else:
        self.handle_departure()
    
    self.print_results()

  def handle_arrival(self):
    self.total_service_users += self.servers_busy * (self.next_arrival - self.time)
    self.total_queue_users += len(self.queue) * (self.next_arrival - self.time)

    self.time = self.next_arrival
    arrival_diff = self.time - self.last_arrival
    self.arrival_differences.append(arrival_diff)
    self.last_arrival = self.time

    if self.is_full() or self.population_size == 0:
      self.file.write(f'{'Usuário rejeitado em':<27}{self.time:>15.5f}\n')
      self.next_arrival = self.time + gen_exponential_time(self.lambda_n())
      return

    self.file.write(f'{'Usuário chega em':<27}{self.time:>15.5f}\n')
    self.population_size -= 1
    self.total_entries += 1
    if self.servers_busy < self.num_servers:
      self.file.write(f'{'Usuário entra em serviço em':<27}{self.time:>15.5f}\n')
      self.servers_busy += 1
      service_time = self.gen_service_time(*self.gen_service_args)
      self.service_times.append(service_time)
      self.insert_departure(self.time + service_time)
    else:
      self.queue.append(self.time)
      
    self.next_arrival = self.time + gen_exponential_time(self.lambda_n())

  def handle_departure(self):
    next_departure = self.next_departures.pop(0)
    self.total_service_users += self.servers_busy * (next_departure - self.time)
    self.total_queue_users += len(self.queue) * (next_departure - self.time)

    self.time = next_departure
    self.file.write(f'{'Usuário sai em':<27}{self.time:>15.5f}\n')
    self.population_size += 1

    if self.next_arrival == float('inf'):
      self.next_arrival = self.time + gen_exponential_time(self.lambda_n())

    if self.queue:
      self.file.write(f'{'Usuário entra em serviço em':<27}{self.time:>15.5f}\n')
      arrival_time = self.queue.pop(0)
      self.total_queue_time += self.time - arrival_time
      service_time = self.gen_service_time(*self.gen_service_args)
      self.service_times.append(service_time)
      self.insert_departure(self.time + service_time)
    else:
      self.servers_busy -= 1
  
  def insert_departure(self, dep: float):
    for i, departure_time in enumerate(self.next_departures):
      if dep < departure_time:
        self.next_departures.insert(i, dep)
        break

  def lambda_n(self):
    return self.lambda_rate if self.population_size < 0 else self.population_size * self.lambda_rate
  
  def is_full(self):
    if self.max_users == -1:
      return False
    return len(self.queue) + self.servers_busy == self.max_users

  def avg_queue_time(self):
    return self.total_queue_time / self.total_entries
  
  def avg_service_time(self):
    return sum(self.service_times) / len(self.service_times)
  
  def avg_system_time(self):
    return self.avg_queue_time() + self.avg_service_time()
  
  def avg_queue_users(self):
    return self.total_queue_users / self.time
  
  def avg_service_users(self):
    return self.total_service_users / self.time
  
  def avg_system_users(self):
    return self.avg_queue_users() + self.avg_service_users()

  def avg_arrival_differences(self):
    return sum(self.arrival_differences) / len(self.arrival_differences)
  
  def var_arrival_differences(self):
    avg = self.avg_arrival_differences()
    return sum((x - avg) ** 2 for x in self.arrival_differences) / (len(self.arrival_differences) - 1)

  def var_service_times(self):
    avg = self.avg_service_time()
    return sum((x - avg) ** 2 for x in self.service_times) / (len(self.service_times) - 1)
  
  def print_results(self):
    print('\nResultados da simulação')
    print(f'{'-> Tempo médio na fila:':<39}',                 '{:>12.5f}'.format(self.avg_queue_time()))
    print(f'{'-> Tempo médio em serviço:':<39}',              '{:>12.5f}'.format(self.avg_service_time()))
    print(f'{'-> Variância dos tempos em serviço:':<39}',     '{:>12.5f}'.format(self.var_service_times()))
    print(f'{'-> Tempo médio no sistema:':<39}',              '{:>12.5f}'.format(self.avg_system_time()))
    print(f'{'-> Tempo médio entre chegadas:':<39}',          '{:>12.5f}'.format(self.avg_arrival_differences()))
    print(f'{'-> Variância do tempo entre chegadas:':<39}',   '{:>12.5f}'.format(self.var_arrival_differences()))
    print(f'{'-> Número médio de usuários na fila:':<39}',    '{:>12.5f}'.format(self.avg_queue_users()))
    print(f'{'-> Número médio de usuários em serviço:':<39}', '{:>12.5f}'.format(self.avg_service_users()))
    print(f'{'-> Número médio de usuários no sistema:':<39}', '{:>12.5f}'.format(self.avg_system_users()))
  
