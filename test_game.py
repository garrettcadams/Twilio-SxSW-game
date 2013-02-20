import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from mock import MagicMock
import sendgrid
from konfig import Konfig
import app as flask_app
from game import Game


def new_game(self, configuration=False):
    default = {'game_default_state': 'intro',
               'game_active': 'true'}
    if not configuration:
        configuration = default
    game = Game()
    game.konf = Konfig()
    game.konf.use_dict(configuration)
    return game


class TestGame(unittest.TestCase):

    def test_game_starts_at_default_start(self):
        game = new_game(configuration={'game_default_state': 'test'})
        self.assertEquals('test', game.state)
        self.assertEquals('sms', game.type)

        game = new_game(configuration={'game_default_state': 'test'},
                        type='voice')
        self.assertEquals('test', game.state)
        self.assertEquals('voice', game.type)

    def test_game_via_voice(self):
        game = new_game(type='voice')

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

        game.next('2')
        self.assertEquals('end', game.state)
        self.assertIn('Congratulations', game.text)

        game.next()
        self.assertEquals('end', game.state)

        game.next('test')
        self.assertEquals('end', game.state)

    def test_game_via_sms(self):
        game = new_game(type='sms')

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

        game.next('1976')
        self.assertEquals('part3', game.state)
        self.assertIn('one question away', game.text)

        game.next('hello world')
        self.assertEquals('end', game.state)
        self.assertIn('Congratulations', game.text)

        game.next()
        self.assertEquals('end', game.state)

        game.next('test')
        self.assertEquals('end', game.state)

    def test_game_start(self):
        game = new_game(type='sms')
        self.assertEquals('start', game.state)

        game = new_game(type='voice')
        self.assertEquals('start', game.state)

    def test_game_intro(self):
        game = new_game(type='sms')
        game.set_state('start')
        game.next('play')
        self.assertEquals('intro', game.state)
        self.assertIn('Do you accept this challenge?', game.response)

        game = new_game(type='voice')
        game.set_state('start')
        game.next('')
        self.assertEquals('intro', game.state)
        self.assertIn('Do you accept this challenge?', game.response)

    def test_game_part1_accept(self):
        game = new_game(type='sms')
        game.set_state('intro')
        game.next('Y')
        self.assertEquals('part1', game.state)
        self.assertIn('Challenge accepted', game.response)

        game = new_game(type='voice')
        game.set_state('intro')
        game.next('1')
        self.assertEquals('part1', game.state)
        self.assertIn('Challenge accepted', game.response)

    def test_game_part1_decline(self):
        game = new_game(type='sms')
        game.set_state('intro')
        game.next('N')
        self.assertEquals('sorry', game.state)
        self.assertIn('Sorry to see you go!', game.response)

        game = new_game(type='voice')
        game.set_state('intro')
        game.next('2')
        self.assertEquals('sorry', game.state)
        self.assertIn('Sorry to see you go!', game.response)

    def test_game_part2(self):
        game = new_game(type='sms')
        game.set_state('part1')
        game.next('hangup')
        self.assertEquals('part2', game.state)
        self.assertIn('In what year was Alexander', game.response)

        game = new_game(type='voice')
        game.set_state('part1')
        game.next('2')
        self.assertEquals('part2', game.state)
        self.assertIn('In what year was Alexander', game.response)

    def test_game_part3(self):
        game = new_game(type='sms')
        game.set_state('part2')
        game.next('1976')
        self.assertEquals('part3', game.state)
        self.assertIn('one question away', game.text)

        game = new_game(type='voice')
        game.set_state('part2')
        game.next('1')
        self.assertEquals('part3', game.state)
        self.assertIn('one question away', game.text)

    def test_game_end(self):
        game = new_game(type='sms')
        game.set_state('part3')
        game.next('hello world')
        self.assertEquals('end', game.state)
        self.assertIn('Congratulations', game.text)

        game = new_game(type='sms')
        game.set_state('end')
        game.next('testing')
        self.assertEquals('end', game.state)
        self.assertIn('Congratulations', game.text)

        game = new_game(type='voice')
        game.set_state('part3')
        game.next('1')
        self.assertEquals('end', game.state)
        self.assertIn('Congratulations', game.text)

        game = new_game(type='voice')
        game.set_state('end')
        game.next('')
        self.assertEquals('end', game.state)
        self.assertIn('Congratulations', game.text)

    def test_game_sorry(self):
        pass

    def test_game_incorrect(self):
        pass
