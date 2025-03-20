from queue_simulator import QueueSimulator, gen_exponential_time, gen_normal_time
    
def get_int(prompt: str, default: int | None = None):
  while True:
    try:
      return int(input(prompt)) if default is None else int(input(prompt) or default)
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
  if service_distribution.startswith("n"):
    mu_mean = get_float("Entre com a média do tempo de serviço: ")
    mu_std_dev = get_float("Entre com o desvio padrão do tempo de serviço: ")
    return (gen_normal_time, (mu_mean, mu_std_dev))
  else:
    mu_rate = get_float("Entre com a taxa de serviço: ")
    return (gen_exponential_time, (mu_rate,))

def get_finite_infinite(prompt_a: str, prompt_b: str):
  len_pop = input(prompt_a).lower()
  if len_pop.startswith("f"):
    population_size = get_int(prompt_b)
  else:
    population_size = -1
  return population_size
  
def main():
  lambda_rate = get_float("Entre com a taxa de chegada: ")
  service_distribution = get_service_distribution()
  num_servers = get_int("Entre com o número de servidores (1): ", 1)
  max_users = get_finite_infinite("Entre com a característica do número máximo de usuários no sistema ([I]nfinita / [f]inita): ", "Entre com o número máimo de usuários no sistema: ")
  population_size = get_finite_infinite("Entre com a característica da população ([I]nfinita / [f]inita): ", "Entre com o tamanho da população: ")
  simulation_time = get_float("Entre com o tempo total de simulação: ")

  simulator = QueueSimulator(lambda_rate, *service_distribution, num_servers, max_users, population_size, simulation_time)
  simulator.simulate()

main()
