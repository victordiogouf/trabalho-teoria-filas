from random import random
from math import sqrt, cos, log, pi

def gen_exponential_time(rate: float):
  return -log(random()) / rate

def gen_normal_time(mean: float, std_dev: float):
  u1 = random()
  u2 = random()
  z = sqrt(-2.0 * log(u1)) * cos(2.0 * pi * u2)
  return mean + std_dev * z

class QueueSimulator:
  # Arrival process is exponential with rate lambda_rate

  def __init__(self, lambda_rate: float, gen_service_time: callable, gen_service_args: tuple, num_servers: int, max_users: int, population_size: int):
    self.lambda_rate = lambda_rate
    self.gen_service_time = gen_service_time
    self.gen_service_args = gen_service_args
    self.num_servers = num_servers
    self.max_users = max_users
    self.population_size = population_size
    self.time = 0
    self.queue = []
    self.next_arrival = gen_exponential_time(lambda_rate)
    self.next_departures = [float('inf')]
    self.servers_busy = 0

    self.total_users = 0
    self.total_queue_time = 0
    self.total_service_time = 0

  def simulate(self, simulation_time: float):
    while self.time < simulation_time:
      if self.next_arrival < self.next_departures[0]:
        # Arrival event
        self.time = self.next_arrival
        if (len(self.queue) + self.servers_busy == self.max_users):
          self.next_arrival = self.time + gen_exponential_time(self.lambda_rate)
          continue
        self.total_users += 1
        if self.servers_busy < self.num_servers:
          self.servers_busy += 1
          service_time = self.gen_service_time(*self.gen_service_args)
          self.total_service_time += service_time
          self.insert_departure(self.time + service_time)
        else:
            self.queue.append(self.time)
        self.next_arrival = self.time + gen_exponential_time(self.lambda_rate)
      else:
        # Departure event
        self.time = self.next_departures.pop(0)
        if self.queue:
          arrival_time = self.queue.pop(0)
          self.total_queue_time += self.time - arrival_time
          service_time = self.gen_service_time(*self.gen_service_args)
          self.total_service_time += service_time
          self.insert_departure(self.time + service_time)
        else:
          self.servers_busy -= 1
  
  def insert_departure(self, dep: float):
    for i, departure_time in enumerate(self.next_departures):
      if dep < departure_time:
        self.next_departures.insert(i, dep)
        break

  def avg_queue_time(self):
    return self.total_queue_time / self.total_users
  
  def avg_service_time(self):
    return self.total_service_time / self.total_users
  
  def avg_system_time(self):
    return self.avg_queue_time() + self.avg_service_time()
  
