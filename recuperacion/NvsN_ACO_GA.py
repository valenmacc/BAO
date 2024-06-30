import ACO
import GA
from ACO.stac.nonparametric_tests import friedman_aligned_ranks_test, shaffer_multitest
import numpy as np
from ACO.Common import Piece
from ACO.Common.fitness import evaluate_fitness
import GA.temp_main

#4 ACO and 4 GA. Each one 31 executions

pieces = Piece.generate_random_pieces(30, 10)

def is_better(a,b):
  return a > b

alpha = 0.05

ACO_h_1 = []
ACO_h_2 = []
ACO_h_3 = []
ACO_h_4 = []

GA_h_1 = []
GA_h_2 = []
GA_h_3 = []
GA_h_4 = []

names = ["ACO_h_1", "ACO_h_2", "ACO_h_3", "ACO_h_4", "GA_h_1", "GA_h_2", "GA_h_3", "GA_h_4"]
names_pos = dict(zip(names, range(len(names))))

for i in range(0,2):#seria hasta 32 para el test bien
  sol,_= ACO(n_ants=3,iterations=3,alpha=0.3,beta=0.6,max_pieces=30,pieces=pieces,x_dim=20,y_dim=20,heuristic=heuristic1)
  ACO_h_1.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
  sol,_ = ACO(n_ants=3,iterations=3,alpha=0.6,beta=0.3,max_pieces=30,pieces=pieces,x_dim=20,y_dim=20,heuristic=heuristic1)
  ACO_h_2.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
  sol,_ = ACO(n_ants=3,iterations=3,alpha=1,beta=0,max_pieces=30,pieces=pieces,x_dim=20,y_dim=20,heuristic=heuristic2)
  ACO_h_3.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
  sol,_ = ACO(n_ants=3,iterations=3,alpha=0,beta=1,max_pieces=30,pieces=pieces,x_dim=20,y_dim=20,heuristic=heuristic1)
  ACO_h_4.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))

  sol = GA.temp_main.GeneticExecution(pieces=pieces, x_dim=20, y_dim=20)
  GA_h_1.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
  sol = GA.temp_main.GeneticExecution(pieces=pieces, x_dim=20, y_dim=20)
  GA_h_2.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
  sol = GA.temp_main.GeneticExecution(pieces=pieces, x_dim=20, y_dim=20)
  GA_h_3.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
  sol = GA.temp_main.GeneticExecution(pieces=pieces, x_dim=20, y_dim=20)
  GA_h_4.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))

_, p_value, rankings, pivots = friedman_aligned_ranks_test(ACO_h_1, ACO_h_2, ACO_h_3, ACO_h_4, GA_h_1, GA_h_2, GA_h_3, GA_h_4)

if p_value < alpha:
  d = dict(zip(names, pivots))
  comp, _, _, adpval = shaffer_multitest(d)

  for i, apv in enumerate(adpval):
    print(comp[i])
    if apv < alpha:
      chunks = comp[i].split("vs")

      name_l = chunks[0].strip()
      name_r = chunks[1].strip()

      if is_better(rankings[names_pos[name_l]], rankings[names_pos[name_r]]):
        print(f"{name_l} is better than {name_r}")
      else:
        print(f"{name_r} is better than {name_l}")
    else:
      print(f"not different")
else:
  print("all variables are the same")