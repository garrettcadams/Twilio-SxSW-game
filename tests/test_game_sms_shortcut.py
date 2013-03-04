import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from game import create_game, add_story_to_game


def new_game(configuration=False):
    default = {'default': 'start2',
               'active': 'true'}
    if not configuration:
        configuration = default
    game = create_game(type='sms')
    print "using configuration: ", configuration
    game.konf.use_dict(configuration)
    game = add_story_to_game(game)
    return game


class TestGameViaSms(unittest.TestCase):

    def test_game_via_sms_with_shortcut(self):
        game = new_game()
        self.assertEquals('start2', game.state)

        game.next('play')
        self.assertEquals('intro2', game.state)
        self.assertIn('Do you accept this challenge?', game.response)

        game.next('Y')
        self.assertEquals('part3', game.state)
        self.assertIn('what phrase is used to verify', game.response)

        game.next('hello world')
        self.assertEquals('end', game.state)
        self.assertIn('Congratulations', game.response)

        game.next('')
        self.assertEquals('end', game.state)

        game.next('test')
        self.assertEquals('end', game.state)
