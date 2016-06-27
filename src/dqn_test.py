#Basic script to test the dqn.py object and functions
import tensorflow as tf
import numpy as np
from dqn import DQN

features = 20
h1 = 10
h2 = 5

g1 = np.arange(40).reshape(2, 20)
g2 = np.random.randint(-5,5,40).reshape(2,20)

dqn = DQN(features, h1, h2, "models/dqn_1")
with tf.Graph().as_default():
    dqn.build_model()
    with tf.Session() as dqn.tf_session:
        dqn._init_tf()
        print(dqn.tf_session.run(dqn.model, feed_dict={dqn.s_: g1}))
    
    

print(dqn.get_q_value(g1, "dqn"))
print(dqn.get_q_value(g1, "dqn"))
print(dqn.get_q_value(g1, "dqn"))
