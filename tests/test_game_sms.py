import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from konfig import Konfig
from game import create_game


def new_game(configuration=False):
    default = {'default': 'intro',
               'active': 'true'}
    if not configuration:
        configuration = default
    game = create_game(type='sms')
    game.konf = Konfig()
    game.konf.use_dict(configuration)
    return game


class TestGame(unittest.TestCase):

    def test_game_starts_at_default_start(self):
        game = new_game(configuration={'default': 'test'})
        self.assertEquals('test', game.state)
        self.assertEquals('sms', game.type)

    def test_game_via_sms(self):
        game = new_game()
        self.assertEquals('start', game.state)

        game.next('play')
        self.assertEquals('intro', game.state)
        self.assertIn('Do you accept this challenge?', game.response)

        game.next('Y')
        self.assertEquals('part1', game.state)
        self.assertIn('Challenge accepted', game.response)

        game.next('hangup')
        self.assertEquals('part2', game.state)
        self.assertIn('In what year was Alexander', game.response)

        game.next('1876')
        self.assertEquals('part3', game.state)
        self.assertIn('one question away', game.response)

        game.next('hello world')
        self.assertEquals('end', game.state)
        self.assertIn('Congratulations', game.response)

        game.next('')
        self.assertEquals('end', game.state)

        game.next('test')
        self.assertEquals('end', game.state)

    def test_game_start(self):
        game = new_game()
        self.assertEquals('start', game.state)

    def test_game_intro(self):
        game = new_game()
        game.set_state('start')
        game.next('play')
        self.assertEquals('intro', game.state)
        self.assertIn('Do you accept this challenge?', game.response)

    def test_game_intro_success(self):
        attempts = ['y', 'Y', 'yes', 'Yes', 'YES',
                    'ok', 'Ok', 'OK', 'sure', 'Sure', 'SURE']
        for attempt in attempts:
            game = new_game()
            game.set_state('intro')
            game.next(attempt)
            self.assertEquals('part1', game.state)
            self.assertIn('Challenge accepted', game.response)

    def test_game_intro_failure(self):
        attempts = ['n', 'N', 'no', 'No', 'NO',
                    'test', 'testing', 'hello there', "what's up"
                    'party', 'Party', 'PARTY']
        for attempt in attempts:
            game = new_game()
            game.set_state('intro')
            game.next(attempt)
            self.assertEquals('start', game.state)
            self.assertIn('Sorry to see you go!', game.response)

    def test_game_part1_success(self):
        attempts = ['hangup', 'Hangup', 'HANGUP',
                    'hang up', 'Hang up', 'HANG UP',
                    'hangup.', 'hang up.',
                    '<hangup>', '<hangup/>', '<HANGUP>']
        for attempt in attempts:
            game = new_game()
            game.set_state('part1')
            game.next(attempt)
            self.assertEquals('part2', game.state)
            self.assertIn('In what year was Alexander', game.response)

    def test_game_part1_failure(self):
        attempts = ['test', 'testing', '123', '1 2 3', 'fake input']
        for attempt in attempts:
            game = new_game()
            game.set_state('part1')
            game.next(attempt)
            self.assertEquals('start', game.state)
            self.assertIn('that is incorrect', game.response)

    def test_game_part2_success(self):
        attempts = ['1876', '18 76', '1876.']
        for attempt in attempts:
            game = new_game()
            game.set_state('part2')
            game.next(attempt)
            self.assertEquals('part3', game.state)
            self.assertIn('one question away', game.response)

    def test_game_part2_failure(self):
        attempts = ['1976', 'test', 'testing', '123', '1 2 3', 'fake input']
        for attempt in attempts:
            game = new_game()
            game.set_state('part2')
            game.next(attempt)
            self.assertEquals('start', game.state)
            self.assertIn('that is incorrect', game.response)

    def test_game_part3_success(self):
        attempts = ['hello world', 'Hello World', 'HELLO WORLD'
                    'Hello world', 'Hello World.', 'HELLO, WORLD']
        for attempt in attempts:
            game = new_game()
            game.set_state('part3')
            game.next(attempt)
            self.assertEquals('end', game.state)
            self.assertIn('Congratulations', game.response)

    def test_game_part3_failure(self):
        attempts = ['goodbye world', 'test', 'testing',
                    '123', '1 2 3', 'fake input']
        for attempt in attempts:
            game = new_game()
            game.set_state('part3')
            game.next(attempt)
            self.assertEquals('start', game.state)
            self.assertIn('that is incorrect', game.response)

    def test_game_end(self):
        attempts = ['', 'hi', 'again', 'party', 'fake']
        for attempt in attempts:
            game = new_game()
            game.set_state('end')
            game.next(attempt)
            self.assertEquals('end', game.state)
