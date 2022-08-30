Instructions for running the game from linux terminal:

1. make new virtual environment:

    virtualenv .stratego -p python3

    source .stratego/bin/activate.csh

2. install requirements:
    
    pip install -r requirements.txt
    
3. run the game from within the environment

    python3 stratego.py [--args]

Example runs:

1. runs a game of human player against smart alpha beta (guessing approach)

With human initialization of starting position:

python3 stratego.py -g gui -ra HumanAgent -ba GuessingAlphaBetaAgent

Without human initialization of starting position:

python3 stratego.py -g gui -ra HumanAgent -ria InitRandomAgent -ba GuessingAlphaBetaAgent


2. run tournament of 4 games between given agents, without display of board (only shows final results)

python3 stratego.py -g console -p 0 -n 4 -ra GuessingAlphaBetaAgent -ba RandomAgent

3. Run a game between alpha beta agent (subset approach) and random agent

python3 stratego.py -g console -d 2 -ra AlphaBetaAgent -rola legal_actions_from_subset_guess -ros 
naive_opp_get_successor -p 2

4. Random against smart agent specifying a heuristic, and an evaluation function (the score printed ats endgame 
   will be using this evaluation function)

python3 stratego.py -g gui -p 1 -ba RandomAgent -ra GuessingAlphaBetaAgent -ria InitHillClimbingAgent -rih 
init_scattering_heuristic -rh naive_unit_count_heuristic -d 1 -n 5 -e naive_unit_value_count_evaluator
    


Explanation about command line arguments:

  -h, --help            show this help message and exit

  -g {console,gui}, --display {console,gui}
                        The game ui.

  -p {0,1,2}, --num_players_to_show {0,1,2}
                        The number of players to show on board - if 2, degrees of soldiers of both sides will be 
                        visible in the UI. If chosen 1, only the degrees of the red player will be visible.

  -d DEPTH, --depth DEPTH
                        The maximum depth for to search in the game tree. Default is 2.

  -n NUM_OF_GAMES, --num_of_games NUM_OF_GAMES
                        The number of games to run. Default is 1.

  -ria {InitRandomAgent,InitHumanAgent,InitHillClimbingAgent}, --red_init_agent {InitRandomAgent,InitHumanAgent,InitHillClimbingAgent}
                        The red init agent - the agent for initial placement of soldiers for red player.

  -bia {InitRandomAgent,InitHumanAgent,InitHillClimbingAgent}, --blue_init_agent {InitRandomAgent,InitHumanAgent,InitHillClimbingAgent}
                        The blue init agent - the agent for initial placement of soldiers for blue player.

  -ra {RandomAgent,HumanAgent,AlphaBetaAgent,GuessingAlphaBetaAgent}, --red_agent {RandomAgent,HumanAgent,AlphaBetaAgent,GuessingAlphaBetaAgent}
                        The red agent.

  -ba {RandomAgent,HumanAgent,AlphaBetaAgent,GuessingAlphaBetaAgent}, --blue_agent {RandomAgent,HumanAgent,AlphaBetaAgent,GuessingAlphaBetaAgent}
                        The blue agent.

  -e EVALUATION_FUNCTION, --evaluation_function EVALUATION_FUNCTION
                        The evaluation function for the game scoring.

  -rih RED_INIT_HEURISTIC, --red_init_heuristic RED_INIT_HEURISTIC
                        The red agent init heuristic (relevant for hill climbing init agent).

  -bih BLUE_INIT_HEURISTIC, --blue_init_heuristic BLUE_INIT_HEURISTIC
                        The blue agent init heuristic (relevant for hill climbing init agent).

  -rh RED_HEURISTIC, --red_heuristic RED_HEURISTIC
                        The red agent heuristic, used to evaluate game states in the search tree. Should be the name 
                        of a function from agents/heuristics.py

  -bh BLUE_HEURISTIC, --blue_heuristic BLUE_HEURISTIC
                        The blue agent heuristic, used to evaluate game states in the search tree.

  -roh RED_OPPONENT_HEURISTIC, --red_opponent_heuristic RED_OPPONENT_HEURISTIC
                        The red agent opponent heuristic - the heuristic that the red agent will assume its opponent 
                        has.

  -boh BLUE_OPPONENT_HEURISTIC, --blue_opponent_heuristic BLUE_OPPONENT_HEURISTIC
                        The blue agent opponent heuristic - the heuristic that the blue agent will assume its opponent 
                        has.

  -rola RED_GET_LEGAL_ACTIONS_OPPONENT, --red_get_legal_actions_opponent RED_GET_LEGAL_ACTIONS_OPPONENT
                        The function used by the red player to estimate the legal actions of his opponent (relevant 
                        when choosing AlphaBetaAgent).

  -bola BLUE_GET_LEGAL_ACTIONS_OPPONENT, --blue_get_legal_actions_opponent BLUE_GET_LEGAL_ACTIONS_OPPONENT
                        The function used by the blue player to estimate the legal actions of his opponent.

  -ros RED_GET_SUCCESSOR_OPPONENTS, --red_get_successor_opponents RED_GET_SUCCESSOR_OPPONENTS
                        The get successor of red player - function used by red player to estimate successors of 
                        opponent actions.

  -bos BLUE_GET_SUCCESSOR_OPPONENTS, --blue_get_successor_opponents BLUE_GET_SUCCESSOR_OPPONENTS
                        The get successor of blue player - function used by blue player to estimate successors of 
                        opponent actions.