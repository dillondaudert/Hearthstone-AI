##AI mechanics
For all files directly related to the AI's functioning

####ai.py
The driver for the AI

####decision-process.py
- build the game tree
- traverse the action tree to evaluate possible actions
- return action decision
- communicate with the trainer to save Markov Decision Process transitions to train on

####trainer.py
- save state transitions <s, a, r>
- update parameters using an experience replay
- uses a target network, updated every t transitions

####dqn.py
- stores deep q learning network to represent the model
- used for the evaluator and the target network in the trainer
