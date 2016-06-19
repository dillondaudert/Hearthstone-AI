#Basic script to test the dqn.py object and functions
import tensorflow as tf
import numpy as np
from ai.dqn import DQN

features = 20
h1 = 10
h2 = 5

g1 = np.arange(40).reshape(2, 20)
g2 = np.random.randint(-5,5,40).reshape(2,20)

dqn = DQN(features, h1, h2)

with tf.Session() as dqn.tf_session:

    dqn.build_model()
    dqn._init_tf()
    for i in range(5):
        print(i)
        print(dqn.get_q_value(g1, "dqn"))
        print(dqn.get_q_value(g1, "target"))


dqn.close()
