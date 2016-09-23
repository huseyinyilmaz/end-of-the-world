from lib.contentparser import read_content
from lib import game

if __name__ == '__main__':
    game.start(read_content('./story.org'))
