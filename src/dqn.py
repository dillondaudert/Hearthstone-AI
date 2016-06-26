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
        self.tf_saver = None

    def _init_tf(self, restore_previous=False, previous_path=None):
        """
        Initialize the variables and other Tensorflow objects
        Args:
            restore_previous: True if restoring a previously trained model
            previous_path: Path to the previous model's saved variables
        Returns:
            self
        """
        init_op = tf.initialize_all_variables()
        self.tf_session.run(init_op)
        print("TF variables initialized!")
        self.tf_saver = tf.train.Saver()
        self.model_path = previous_path

        if restore_previous:
            self.tf_saver.restore(self.tf_session, previous_path)

    def build_model(self):
        """
        Build the network model.
        Args:
            None
        Returns:
            self
        """
    
        #A game state
        self.s_ = tf.placeholder(tf.float32, shape=[None, self.features])

        with tf.variable_scope("dqn") as dqn:
            model = self._dqn_eval()

        with tf.variable_scope("target") as target:
            target = self._dqn_eval()

            


    def get_q_value(self, g_state, v_scope):
        """
        Get the q value of a particular game state
        Args:
            g_state: A game state numpy array
            v_scope: The variable scope to use; either dqn or target network
        Returns:
            q_val: The Q value associated with this state (i.e. this action)
        """
        with tf.variable_scope(v_scope, reuse=True):
            q_val = self._dqn_eval()

        return self.tf_session.run(q_val, feed_dict={self.s_: g_state})

        

    def _relu(self, input, l_shape, b_shape):
        #Create weights variable
        weights = tf.get_variable("weights", l_shape, initializer=tf.random_normal_initializer(0.0, stddev=0.35))
        #Create biases
        biases = tf.get_variable("biases", b_shape, initializer=tf.constant_initializer(0.0))
        #Return layer calculation
        op = tf.nn.relu(tf.matmul(input, weights) + biases)
        return op

    def _dqn_eval(self):
        with tf.variable_scope('hidden1'):
            hidden1 = self._relu(self.s_, [self.features, self.h1_units] , [self.h1_units])
        with tf.variable_scope('hidden2'):
            hidden2 = self._relu(hidden1, [self.h1_units, self.h2_units], [self.h2_units])
        with tf.variable_scope('hidden3'):
            hidden3 = self._relu(hidden2, [self.h2_units, 1], [1])
        return hidden3


    def close(self):
        """
        Close the session
        Args:
        Returns:
            self
        """
        self.tf_session.close()
