from agents.human_agent import HumanAgent
from agents.init_agents.init_hill_climbing_agent import InitHillClimbingAgent
from agents.init_agents.init_random_agent import InitRandomAgent
from agents.random_agent import RandomAgent
from game import StrategoGame
from graphics.console_graphic import ConsoleGraphic
from graphics.gui_graphic import GuiGraphic
from soldier import Color
from agents.init_agents.init_heuristics import *

if __name__ == '__main__':
    # graphic = ConsoleGraphic(10, 2)
    graphic = GuiGraphic(10, 2)
    red_agent = HumanAgent(Color.RED, graphic, InitHillClimbingAgent(try_heuristic))
    blue_agent = RandomAgent(Color.BLUE, graphic, InitRandomAgent())
    game = StrategoGame(red_agent, blue_agent, graphic, True)
    score = game.run()

