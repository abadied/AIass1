Running the algorithms:
after entering the amount and the positions of stains and fruits please enter v for value iteration algorithm or p for
policy iteration (get_policy method responsible for that).

Constants for graphs:
  a. seconds_per_period
  b. iterations_per_period
  c. plot_graph
  if you want to find the policy without plotting the graphs (plotting the graphs affects running time performance)
   please change the value of 'plot_graph' to false
  
 Optimization
  value iteration:
  a. get_possible_states: when updating state using bellman equation we only run over the possible states the robot can
   reach from that state. we get the possible states for state S by checking the next actual state for each legal action in state S.
  b. initiate_value_function: we create an initial value function with a pessimist estimate for each state.
  c. value_iteration, calc_value_and_action_for_curr_state: value iteration simulates value iteration algorithm, we use
   calc_value_and_action_for_curr_state for finding the optimal action and maximum value for each state in each iteration
    until convergence, also we calculate and update in real time the value function instead of saving copies of it.
  
 Policy iteration:
 a. get_possible_states: when updating state using bellman equation we only run over the possible states the robot can
  reach from that state. we get the possible states for state S by checking the next actual state for each legal action
   in state S.
 b. get_initial_policy: initiate 'smart' policy by checking for each state what is the most likable action for each state.
  for example:  state in which the robot`s position is the same as the position of one of the stains the initiate action
   in "clean", the same for fruits and "pick" and for "put in basket" - when the robot position is the same as basket
    position and he already picked some fruits.
 c. get_action: in case the position of the robot is in empty cell, the method above use this function in order to find
  the direction to stain, fruit or the basket.
 d. policy_iteration, set_value_function: policy iteration simulates policy iteration algorithm, we use
 set_value_function in order to find the matching value function the the given policy according to gamma and epsilon,
  we updates several states in the policy in each iteration in order to accelerate calculation time of the new policy
  and the relevant value function.
 
 Plotting graphs:
 a. collect_and_plot_graph_data: This function runs by a separated thread and writes every constant amount of time the average
    of the value function at that specific time.
 b. plotting bu iterations: every constant amount of iteration, both methods (value/policy) computes the average of
  the value function and save it with its corresponding number of iteration.
 
 Configurations:
 board: 4 on 4 combinations with fruits and stains.
 board: 5 on 5, all possible scattering of fruits and/or stains
 board: 7 on 7, 2 stains and 2 fruits
 board: 10 on 10, 2 stains and 2 fruits (work fast without plotting the graphs)