#Test calling q value function from multiple processes
import tensorflow as tf
import numpy as np
from dqn import DQN
import multiprocessing as mp
import sys

def q_par(dqn, g1):
    print(dqn.get_q_value(g1, "dqn"))

def par(a):
    print(a)

features = 20
h1 = 10
h2 = 5

g1 = np.arange(40).reshape(2, 20)

dqn = DQN(features, h1, h2, "models/tf_multi_1")
with dqn.tf_graph.as_default():
    dqn.build_model()
    with tf.Session() as dqn.tf_session:
        dqn._init_tf()
        print(dqn.tf_session.run(dqn.model, feed_dict={dqn.s_: g1}))

processes = []

for p in range(4):
    processes.append(mp.Process(target=q_par, args=(dqn,g1)))
    processes[p].start()

for p in range(4):
    processes[p].join()
