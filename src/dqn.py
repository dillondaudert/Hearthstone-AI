#dqn.py
#The model for the game state. This is used to evaluate a state.

import tensorflow as tf

class DQN(object):
    """
    An object representing a Deep Q Learning Network
    """
    def __init__(self, features, h1_units, h2_units, model_path=None):
        """
        Initializes the network model object.
        Args:
            features: The size of the feature vector input
            h1_units: The number of units in the first hidden layer
            h2_units: The number of units in the second hidden layer
            model_path: The path to saved state of this model
        Returns:
            self
        """
        self.features = features
        self.h1_units = h1_units
        self.h2_units = h2_units

        #Tensorflow objects for the AI
        self.tf_session = None
        self.tf_saver = None
        self.tf_graph = tf.Graph()

        self.model_path = model_path

    def _init_tf(self, restore_previous=False):
        """
        Initialize the variables and other Tensorflow objects
        Args:
            restore_previous: True if restoring a previously trained model
        Returns:
            self
        """
        init_op = tf.initialize_all_variables()
        self.tf_saver = tf.train.Saver()
        self.tf_session.run(init_op)

        if restore_previous:
            self.tf_saver.restore(self.tf_session, self.model_path)
        else:
            self.tf_saver.save(self.tf_session, self.model_path)


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
            self.model = self._dqn_eval()

        with tf.variable_scope("target") as target:
            self.target = self._dqn_eval()
        
    def train_model(self):
        """
        Train model on a sample from experience replay.
        """
        pass

    def _train_step(self):
        """
        Do one training step. Calculate loss, backpropagate errors.
        """
        pass    


    def get_q_value(self, g_state, v_scope):
        """
        Get the q value of a particular game state.
        Builds the graph, restores previous model (if applicable), runs session.
        Args:
            g_state: A game state numpy array
            v_scope: The variable scope to use; either dqn or target network
            restore_previous: True if restoring previous model from self.model_path
        Returns:
            q_val: The Q value associated with this state (i.e. this action)
        """
        
        with self.tf_graph.as_default():
            #self.build_model()
            
            with tf.Session() as self.tf_session:
                self._init_tf(True) 
                with tf.variable_scope(v_scope, reuse=True):
                    q_val = self._dqn_eval()
                ret = self.tf_session.run(q_val, feed_dict={self.s_: g_state})

        return ret

        

    def _relu(self, input, l_shape, b_shape):
        #Create weights variable
        weights = tf.get_variable("weights", l_shape, initializer=tf.random_uniform_initializer(-1, 1))
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
