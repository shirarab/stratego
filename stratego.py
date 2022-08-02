from agents.human_agent import HumanAgent
from agents.init_agents.init_random_agent import InitRandomAgent
from agents.random_agent import RandomAgent
from game import StrategoGame
from graphics.console_graphic import ConsoleGraphic
from graphics.gui_graphic import GuiGraphic
from soldier import Color

if __name__ == '__main__':
    # graphic = ConsoleGraphic(10, 0)
    graphic = GuiGraphic(10, 1)
    red_agent = RandomAgent(Color.RED, graphic, InitRandomAgent())
    blue_agent = RandomAgent(Color.BLUE, graphic)
    game = StrategoGame(red_agent, blue_agent, graphic, True)
    score = game.run()
