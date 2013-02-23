import re
from konfig import Konfig


class GameState:
    def __init__(self, name):
        self.name = name
        self.text = ''
        self.solved = False
        self.success_if = {'sms': [], 'voice': []}
        self.success = ''
        self.failure = ''
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

    def to_twiml(self, type):
        return self.text

    def send_input(self, attempt):
        print "attempt: '%s'" % attempt
        needle = self.cleanup(attempt)
        haystack = self.success_if[self.type]
        print "haystack for %s is %s" % (self.name, str(haystack))
        if len(haystack) == 1 and haystack[0] is True:
            self.solved = True
        elif needle in haystack:
            self.solved = True


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
            print "default() returning: 'start'"
            return 'start'

    @property
    def state(self):
        if not self.current_state:
            self.set_state(self.default)
        print "STATE: '%s'" % self.current_state.name
        return self.current_state.name

    def add_state(self, state):
        state.type = self.type
        state.default = self.default
        print "state.default: ", state.default
        self.states[state.name] = state

    def set_state(self, state_name):
        self.current_state = self.states[state_name]

    def next(self, attempt=False):
        self.current_state.send_input(attempt)
        if self.current_state.solved:
            self.current_state = self.states[self.current_state.next]
            self.response = self.current_state.text
        else:
            self.response = self.current_state.text_fail
            self.current_state = self.states[self.default]
        print "Response is: '%s'" % self.response


def create_game(type='sms'):
    return NewGame(type)


def add_story_to_game(game):
    state = GameState('start')
    state.next = 'intro'
    state.sms_success_if([True])
    state.text_fail = False
    game.add_state(state)

    message_sorry = 'Sorry to see you go!'
    message_incorrect = 'that is incorrect'

    state = GameState('intro')
    state.next = 'part1'
    state.text = 'Do you accept this challenge?'
    state.text_fail = message_sorry
    state.sms_success_if(['y', 'yes', 'ok', 'okay', 'sure'])
    game.add_state(state)

    state = GameState('part1')
    state.next = 'part2'
    state.text = 'Challenge accepted'
    state.text_fail = message_incorrect
    state.sms_success_if(['hangup', 'hang up'])
    game.add_state(state)

    state = GameState('part2')
    state.next = 'part3'
    state.text = 'In what year was Alexander'
    state.text_fail = message_incorrect
    state.sms_success_if(['1876'])
    game.add_state(state)

    state = GameState('part3')
    state.next = 'end'
    state.text = 'one question away'
    state.text_fail = message_incorrect
    state.sms_success_if(['hello world'])
    game.add_state(state)

    state = GameState('end')
    state.next = 'end'
    state.text = 'Congratulations'
    state.sms_success_if([True])
    game.add_state(state)

    return game
