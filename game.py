import re
from konfig import Konfig
from twilio import twiml


class GameState:
    def __init__(self, name):
        self.name = name
        self.text = ''
        self.solved = False
        self.success_if = {'sms': [], 'voice': []}
        self.success = ''
        self.failure = ''
        self.options = []
        self.pattern = re.compile('[\W_]+')

    def cleanup(self, input):
        if isinstance(input, str):
            text = str(input).upper()
            return self.pattern.sub('', text)
        else:
            return input

    def set_success_if(self, type, options):
        rv = map(lambda x: self.cleanup(x), options)
        self.success_if[type] = rv

    def sms_success_if(self, options):
        self.set_success_if('sms', options)

    def voice_success_if(self, options):
        self.set_success_if('voice', options)

    def voice_options(self, options):
        self.options = options

    def send_input(self, attempt):
        needle = self.cleanup(attempt)
        haystack = self.success_if[self.type]
        print ".send_input(%s): haystack: %s" % (attempt, str(haystack))
        if len(haystack) == 1 and haystack[0] is True:
            self.solved = True
        elif needle in haystack:
            self.solved = True
        print ".send_input(%s) = %s" % (attempt, str(self.solved))


class NewGame:
    def __init__(self, type):
        self.type = type
        self.konf = Konfig()
        self.current_state = False
        self.states = {}

    @property
    def default(self):
        if self.konf.default:
            return self.konf.default
        else:
            return 'start'

    @property
    def state(self):
        if not self.current_state:
            self.set_state(self.default)
        return self.current_state.name

    def add_state(self, state):
        state.type = self.type
        state.default = self.default
        self.states[state.name] = state

    def set_state(self, state_name):
        self.current_state = self.states[state_name]

    def to_twiml(self, input):
        r = twiml.Response()
        if self.type is 'sms':
            r.sms(input)
            return(str(r))
        elif self.type is 'voice':
            r.say(input)
            gather = r.gather()
            for option in self.current_state.options:
                text = 'Press %s' % (option)
                gather.say(text)
            return(str(r))
        else:
            return input

    def next(self, attempt=False):
        if not self.state:
            print "Error determining state"
        self.current_state.send_input(attempt)
        if self.current_state.solved:
            self.current_state = self.states[self.current_state.next]
            self.response = self.to_twiml(self.current_state.text)
        else:
            self.response = self.to_twiml(self.current_state.text_fail)
            self.current_state = self.states[self.default]


def create_game(type='sms'):
    return NewGame(type)


def add_story_to_game(game):
    state = GameState('start')
    state.next = 'intro'
    state.sms_success_if([True])
    state.voice_success_if([True])
    state.text_fail = False
    game.add_state(state)

    state = GameState('shortcut')
    state.next = 'part3'
    state.sms_success_if([True])
    state.voice_success_if([True])
    state.text_fail = False
    game.add_state(state)

    message_sorry = ('Sorry to see you go! '
                     'Make sure to follow @twilio on Twitter '
                     'for updates around SxSW 2013.')
    message_incorrect = ('Oh no, '
                         'that is incorrect. Fear not! '
                         'You can start from the beginning to try again.')

    state = GameState('intro')
    state.next = 'part1'
    state.text = ("To get on the list for Twilio's SxSW party, "
                  "you must answer three questions "
                  "to prove your Twilio street cred. "
                  "Do you accept this challenge?")
    state.text_fail = message_sorry
    state.sms_success_if(['y', 'yes', 'ok', 'okay', 'sure'])
    state.voice_options(['1 to accept',
                         '2 to decline'])
    state.voice_success_if(['1'])
    game.add_state(state)

    state = GameState('part1')
    state.next = 'part2'
    state.text = ('Challenge accepted. '
                  'Answer this correctly to proceed. '
                  'Which TwiML verb ends a call?')
    state.text_fail = message_incorrect
    state.sms_success_if(['hangup', 'hang up'])
    state.voice_options(['1 for Reject',
                         '2 for Hangup',
                         '3 for Leave'])
    state.voice_success_if(['2'])
    game.add_state(state)

    state = GameState('part2')
    state.next = 'part3'
    state.text = ('You have two questions remaining: '
                  'In what year was Alexander Graham Bell '
                  'awarded the patent for the telephone?')
    state.text_fail = message_incorrect
    state.sms_success_if(['1876'])
    state.voice_options(['1 for 18 76',
                         '2 for 18 75',
                         '3 for The patent is actually held by Elisha Gray'])
    state.voice_success_if(['1'])
    game.add_state(state)

    state = GameState('part3')
    state.next = 'end'
    state.text = ("When initially testing your very first Twilio app, "
                  "what phrase is used to verify it is working correctly?")
    state.text_fail = message_incorrect
    state.sms_success_if(['hello world', 'hello monkey'])
    state.voice_options(['1 for popcorn',
                         '2 for ahoy',
                         '3 for hello monkey'])
    state.voice_success_if(['3'])
    game.add_state(state)

    state = GameState('end')
    state.next = 'end'
    state.text = ("Congratulations, we'd be honored to have you at our party. "
                  "Register at: http://twiliosxsw2013.eventbrite.com "
                  "password: %s") % (game.konf.game_password)
    state.sms_success_if([True])
    state.voice_success_if([True])
    game.add_state(state)

    return game
