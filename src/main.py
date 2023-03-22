from game import Game
from game_loop import Run

def main():
    game = Game()
    game_loop = Run(game)


if __name__ == "__main__":
    main()