#dqn.py
#The model for the game state. This is used to evaluate a state.

import tensorflow as tf

class DQN(object):
    """
    An object representing a Deep Q Learning Network
    """
    def __init__(self, features, h1_units, h2_units):
        """
        Initializes the network model object.
        Args:
            features: The size of the feature vector input
            h1_units: The number of units in the first hidden layer
            h2_units: The number of units in the second hidden layer
        Returns:
            self
        """
        self.features = features
        self.h1_units = h1_units
        self.h2_units = h2_units

        #Tensorflow objects for the AI
        self.tf_session = None
        self.tf_saver = tf.train.Saver()

    def build_model(self):
        """
        Build the network model.
        Args:
            None
        Returns:
            self
        """
    
        #A game state
        s_ = tf.placeholder(tf.float32, shape=(self.features, 1))

        with tf.variable_scope("dqn") as dqn:
            model = self._dqn_eval(s_)

        with tf.variable_scope("target") as target:
            target = self._dqn_eval(s_)

        init_op = tf.initialize_all_variables()
        with tf.Session() as self.tf_session:
            self.tf_session.run(init_op)
            print("TF variables initialized!")


    def get_q_value(g_state, v_scope):
        """
        Get the q value of a particular game state
        Args:
            g_state: A game state numpy array
            v_scope: The variable scope to use; either dqn or target network
        Returns:
            q_val: The Q value associated with this state (i.e. this action)
        """
        with tf.variable_scope(v_scope, reuse=True):
            q_val = self._dqn_eval(g_state)

        return q_val

        

    def _relu(self, input, l_shape, b_shape):
        #Create weights variable
        weights = tf.get_variable("weights", l_shape, initializer=tf.random_normal_initializer(0, stddev=0.35))
        #Create biases
        biases = tf.get_variable("biases", b_shape, tf.constant_initializer(0))
        #Return layer calculation
        op = tf.nn.relu(tf.matmul(weights, input) + biases)
        return op

    def _dqn_eval(self, input_state):
        with tf.variable_scope('hidden1'):
            hidden1 = self._relu(input_state, [self.h1_units, self.features] , [self.features])
        with tf.variable_scope('hidden2'):
            hidden2 = self._relu(hidden1, [self.h2_units, self.h1_units], [self.h1_units])
        with tf.variable_scope('hidden3'):
            hidden3 = self._relu(hidden2, [1, self.h2_units], [self.h2_units])
        return hidden3

    def e
