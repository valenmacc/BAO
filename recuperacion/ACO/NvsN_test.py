from stac.nonparametric_tests import friedman_aligned_ranks_test, shaffer_multitest
from ACO import ACO
from Common.heuristic import *
from Common.Piece import Piece


pieces = Piece.generate_random_pieces(30, 10)

def is_better(a,b):
  return a > b

alpha = 0.05

h_1 = []
h_2 = []
h_3 = []
h_4 = []
names = ["h_1", "h_2", "h_3", "h_4"]
names_pos = dict(zip(names, range(len(names))))

for i in range(0,2):#seria hasta 32 para el test bien
    sol,temp = ACO(n_ants=3,iterations=3,alpha=0.3,beta=0.6,max_pieces=30,pieces=pieces,x_dim=20,y_dim=20,heuristic=heuristic1)
    h_1.append(sol)
    sol,temp = ACO(n_ants=3,iterations=3,alpha=0.6,beta=0.3,max_pieces=30,pieces=pieces,x_dim=20,y_dim=20,heuristic=heuristic1)
    h_2.append(sol)
    sol,temp = ACO(n_ants=3,iterations=3,alpha=0.3,beta=0.6,max_pieces=30,pieces=pieces,x_dim=20,y_dim=20,heuristic=heuristic2)
    h_3.append(sol)
    sol,temp = ACO(n_ants=3,iterations=3,alpha=0.6,beta=0.3,max_pieces=30,pieces=pieces,x_dim=20,y_dim=20,heuristic=heuristic2)
    h_4.append(sol)

_, p_value, rankings, pivots = friedman_aligned_ranks_test(h_1, h_2, h_3, h_4)

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