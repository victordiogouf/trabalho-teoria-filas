from queue_simulator import QueueSimulator, gen_exponential_time, gen_normal_time
    
def get_int(prompt: str):
  while True:
    try:
      return int(input(prompt))
    except ValueError:
      print("Valor inválido. Tente novamente.")

def get_float(prompt: str):
  while True:
    try:
      return float(input(prompt))
    except ValueError:
      print("Valor inválido. Tente novamente.")   

def get_service_distribution():
  service_distribution = input("Entre com a distribuição do tempo de serviço ([E]xponencial / [n]ormal): ").lower()
  if service_distribution == 'n':
    mu_mean = get_float("Entre com a média do tempo de serviço: ")
    mu_std_dev = get_float("Entre com o desvio padrão do tempo de serviço: ")
    return (gen_normal_time, (mu_mean, mu_std_dev))
  else:
    mu_rate = get_float("Entre com a taxa de serviço: ")
    return (gen_exponential_time, (mu_rate,))
  
def main():
  # Taxa de chegada
  lambda_rate = get_float("Entre com a taxa de chegada: ")
  service_distribution = get_service_distribution()
  num_servers = get_int("Entre com o número de servidores: ")
  max_users = get_int("Entre com o número máximo de usuários no sistema: ")
  population_size = get_int("Entre com o tamanho da população: ")
  simulation_time = get_float("Entre com o tempo total de simulação: ")

  simulator = QueueSimulator(lambda_rate, *service_distribution, num_servers, max_users, population_size)
  simulator.simulate(simulation_time)
  
  print("Tempo médio de espera na fila:", simulator.avg_queue_time())
  print("Tempo médio de serviço:", simulator.avg_service_time())
  print("Tempo médio no sistema:", simulator.avg_system_time())

main()