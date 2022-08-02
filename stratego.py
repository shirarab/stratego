from agents.human_agent import HumanAgent
from agents.init_agents.init_random_agent import InitRandomAgent
from agents.random_agent import RandomAgent
from game import StrategoGame
from graphics.basic_stratego_graphic import BasicStrategoGraphic
from soldier import Color

if __name__ == '__main__':
    graphic = BasicStrategoGraphic(10, 2)
    red_agent = HumanAgent(Color.RED, graphic, InitRandomAgent())
    blue_agent = RandomAgent(Color.BLUE, graphic)
    game = StrategoGame(red_agent, blue_agent, graphic)
    score = game.run()
    print(score)
