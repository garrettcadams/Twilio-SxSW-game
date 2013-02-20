import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from konfig import Konfig
from game import Game


def new_game(configuration=False):
    default = {'game_default_state': 'intro',
               'game_active': 'true'}
    if not configuration:
        configuration = default
    game = Game(type='voice')
    game.konf = Konfig()
    game.konf.use_dict(configuration)
    return game


class TestGame(unittest.TestCase):

    def test_game_starts_at_default_start(self):
        game = new_game(configuration={'game_default_state': 'test'})
        self.assertEquals('test', game.state)
        self.assertEquals('sms', game.type)

    def test_game(self):
        game = new_game()
        self.assertEquals('start', game.state)

        game.next('')
        self.assertEquals('intro', game.state)
        self.assertIn('Do you accept this challenge?', game.response)

        game.next('1')
        self.assertEquals('part1', game.state)
        self.assertIn('Challenge accepted', game.response)

        game.next('2')
        self.assertEquals('part2', game.state)
        self.assertIn('In what year was Alexander', game.response)

        game.next('1')
        self.assertEquals('part3', game.state)
        self.assertIn('one question away', game.text)

        game.next('3')
        self.assertEquals('end', game.state)
        self.assertIn('Congratulations', game.text)

        game.next()
        self.assertEquals('end', game.state)

        game.next('1')
        self.assertEquals('end', game.state)

    def test_game_start(self):
        game = new_game()
        self.assertEquals('start', game.state)

    def test_game_intro(self):
        game = new_game()
        game.set_state('start')
        game.next('')
        self.assertEquals('intro', game.state)
        self.assertIn('Do you accept this challenge?', game.response)
        self.assertIn('Press 1 for', game.response)
        self.assertIn('Press 2 for', game.response)
        self.assertIn('Press 3 for', game.response)

    def test_game_intro_success(self):
        attempts = ['1']
        for attempt in attempts:
            game = new_game()
            game.set_state('intro')
            game.next(attempt)
            self.assertEquals('part1', game.state)
            self.assertIn('Challenge accepted', game.response)

    def test_game_intro_failure(self):
        attempts = ['2', '3', '4', '99']
        for attempt in attempts:
            game = new_game()
            game.set_state('intro')
            game.next(attempt)
            self.assertEquals('start', game.state)
            self.assertIn('Sorry to see you go!', game.response)

    def test_game_part1_success(self):
        attempts = ['2']
        for attempt in attempts:
            game = new_game()
            game.set_state('part1')
            game.next(attempt)
            self.assertEquals('part2', game.state)
            self.assertIn('In what year was Alexander', game.response)
            self.assertIn('Press 1 for', game.response)
            self.assertIn('Press 2 for', game.response)
            self.assertIn('Press 3 for', game.response)

    def test_game_part1_failure(self):
        attempts = ['1', '3', '4', '5', '99']
        for attempt in attempts:
            game = new_game()
            game.set_state('part1')
            game.next(attempt)
            self.assertEquals('start', game.state)
            self.assertIn('that is incorrect', game.response)

    def test_game_part2_success(self):
        attempts = ['1']
        for attempt in attempts:
            game = new_game()
            game.set_state('part2')
            game.next(attempt)
            self.assertEquals('part3', game.state)
            self.assertIn('one question away', game.text)
            self.assertIn('Press 1 for', game.response)
            self.assertIn('Press 2 for', game.response)
            self.assertIn('Press 3 for', game.response)

    def test_game_part2_failure(self):
        attempts = ['2', '3', '4', '5', '99']
        for attempt in attempts:
            game = new_game()
            game.set_state('part2')
            game.next('2')
            self.assertEquals('start', game.state)
            self.assertIn('that is incorrect', game.response)

    def test_game_part3_success(self):
        attempts = ['3']
        for attempt in attempts:
            game = new_game()
            game.set_state('part3')
            game.next(attempt)
            self.assertEquals('end', game.state)
            self.assertIn('Congratulations', game.text)

    def test_game_part3_failure(self):
        attempts = ['1', '2', '4', '5', '99']
        for attempt in attempts:
            game = new_game()
            game.set_state('part3')
            game.next(attempt)
            self.assertEquals('start', game.state)
            self.assertIn('that is incorrect', game.response)

    def test_game_end(self):
        attempts = ['', '1', '2', '3', '4', '5', '99']
        for attempt in attempts:
            game = new_game()
            game.set_state('end')
            game.next(attempt)
            self.assertEquals('end', game.state)
