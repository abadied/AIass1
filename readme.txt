after entering the amount and the positions of stains and fruits please enter v for value iteration algorithm or p for policy iteration (get_policy method responsible for that).
Constants for graphs:
  a. seconds_per_period
  b. iterations_per_period
  c. plot_graph
  if you want to find the policy without plotting the graphs (plotting the graphs affects running time performance) please change the value   of 'plot_graph' to faulse
  
 Optimization
  value iteration:
  a. get_possible_states: when updating state using bellman equation we only run over the possible states the robot can reach from that          state. we get the possible states for state S by checking the next actual state for each legal action in state S.
  b. initiate_value_function: we give priority for states in which the robot cleaned staints and picked fruits by giving them non-negative      reward
  c. value_iteration, calc_value_and_action_for_curr_state: value iteration simulates value iteration algorithm, we use                          calc_value_and_action_for_curr_state for finding the optimal action and maximum value for each state in each iteration until                convergence 
  
 Policy iteration:
 a. get_possible_states: when updating state using bellman equation we only run over the possible states the robot can reach from that          state. we get the possible states for state S by checking the next actual state for each legal action in state S.
 b. get_random_policy: initiate 'smart' policy by checking for each state what is the most likable action for each state. for example:     state in which the robot`s position is the same as the position of one of the stains the initiate action in "clean", the same for           fruits and "pick" and for "put in basket" - when the robot position is the same as baket positon and he already picked some fruits.
 c. get_action: in case the position of the robot is in empy cell, the method above use this function in order to find the direction to         stain, fruit or the basket. 
 c. policy_iteration, set_value_function: policy iteration simulates policy iteration algorithm, we use set_value_function in order to find     the matching value function the the given policy according to gamma and epsilon
 
 Plotting graphs:
 a. collect_and_plot_graph_data: This function runs by a separated thread and writes every constant amount of time the average
    of the value function at that specific time.
 b. value_iteration: every constant amount of iteration, the method computes the average of the value function
 
 Configurations:
 board: 5 on 5, all possible scattering of fruits and/or stains
 board: 7 on 7, 2 stains and 2 fruits
 board: 10 on 10, 2 stains and 2 fruits (work fast without plotting the graphs)