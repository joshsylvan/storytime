"""Storyline handling."""
import random
import jinja2

from .emitters import emit_narrator, emit_input, emit_choice

PLAYERS = {}

CURRENT_STORY = None


class Story:
    players = []
    data = None
    mapping = None

    def get_next(self):
        return self.next

    def render_data(self):
        print(f'templating {self.data}')
        text = ""
        template = jinja2.Template(str(self.data))
        player_mapping = {}
        for sid, player in PLAYERS.items():
            print(f'player:{player.__dict__}')
            for item, value in self.mapping.items():
                sid_value = "_".join(item.split("_")[1:])
                sid_value = f"{sid_value}_{sid}"
                player_mapping[sid_value] = getattr(player, value)
        print("mapping:", player_mapping)
        text += template.render(player_mapping)
        return text


class StoryNarration(Story):
    def __init__(self, name, data, mapping=None):
        self.name, self.data = name, data
        self.mapping = mapping

    def emit(self):
        text = super().render_data()
        text = text.split('. ')
        print(text)
        emit_narrator(text)


class StoryInput(Story):
    def __init__(self, name, data):
        self.name, self.data = name, data
        self.next = None

    def emit(self):
        emit_input(self)


class StoryDecision(Story):
    def __init__(self, name, data):
        self.name, self.data = name, data
        self.left, self.right = None, None

    def get_next(self):
        return [next_story if len(next_story.players) > 0 else None for next_story in [self.left, self.right]]

    def get_name(self):
        pass

    def emit(self):
        emit_choice(self)


class Player:
    def __init__(self, name, honorific):
        self.name = name
        self.honorific = honorific
        self.has_responded = None
        self.responses = {}


def construct_template(players, template, template_vars):
    """For every player, extract template_vars from player and fill into template."""
    player_sentences = []
    for sid in PLAYERS.keys():
        player_vars = ['{{ %s }}' % f'{var}_{sid}' for var in template_vars]
        text = template.format(*player_vars)
        player_sentences.append(text)
    all_sentences = ' '.join(player_sentences)
    return all_sentences


def construct_story():
    """"""
    # Disguise: what are players wearing
    intro = StoryNarration('intro', 'You are in front of this mansion. What are you wearing?')

    # Gift: what gifts have been brought
    disguise = StoryInput('disguise', 'What disguise are you wearing?')
    template_mapping = {'player_fullname': 'fullname', 'player_response_disguise': 'response_disguise'}
    wearing = construct_template(PLAYERS, '{0} is wearing {1}.', template_mapping.values())
    entering_text = f'{wearing} You enter the mansion. People greet you and ask what gift you brought.'
    entering = StoryNarration('entering', entering_text, template_mapping)
    gift = StoryInput('gift', 'What gift did you bring?')

    template_mapping = {'player_fullname': 'fullname', 'player_response_gift': 'response_gift'}
    gifting = construct_template(PLAYERS, '{0} brought {1}.', template_mapping.values())
    thanks_text = f'{gifting} You may enter. You approach some party people, what do you say?'
    thanks = StoryNarration('thanks', thanks_text, template_mapping)

    # Mingle: speak with people
    mingle = StoryInput('mingle', 'You approach some people, what do you say?')
    template_mapping = {'player_fullname': 'fullname', 'player_response_mingle': 'response_mingle'}
    player_icebreakers = construct_template(PLAYERS, '{0} says: "{1}".', template_mapping.values())
    awkward_text = f'{player_icebreakers} The guests ignore you - they are disgusted by your lack of respect. You need to find Hitler.'
    awkward = StoryNarration('awkward', awkward_text, template_mapping)

    # party split
    search = StoryDecision('search', {'question': 'Where do you go to find Hitler himself?', 'choices': ['Garden', 'Library']})
    garden = StoryInput('garden', 'What you drinking fam?')
    library = StoryInput('library', "What do you think of Hitler's painting?")

    search.left = garden
    search.right = library
    awkward.next = search
    mingle.next = awkward
    thanks.next = mingle
    gift.next = thanks
    entering.next = gift
    disguise.next = entering
    intro.next = disguise

    return intro


def start():
    global CURRENT_STORY
    CURRENT_STORY = construct_story()

def get_story_text():
    global CURRENT_STORY
    story_text = CURRENT_STORY.data.split('. ')
    return story_text


def advance_story():
    global CURRENT_STORY
    next_story = CURRENT_STORY.get_next()
    print(f'story: current={CURRENT_STORY.name}, next={next_story.name}')
    CURRENT_STORY = next_story
    CURRENT_STORY.emit()


def get_honorific():
    honorifics = [
        'great', 'emperor', 'child', 'jester', 'captain', 'fool', 'cunt', 'king', 'donkey', 'devil',
        'faceless', 'queen', 'young', 'bold', 'timid', 'peasant', 'big man', 'monster', 'maniac', 'flamboyant',
        'jockey', 'giant', 'weak', 'poor', 'farmer', 'knight', 'animal', 'predator', 'strangled', 'drowned',
        'smelly', 'fork', 'bitch', 'pleb', 'brave', 'coward', 'legless', 'nugget', 'fallen', 'forsaken',
        'grey', 'fat', 'ugly', 'sad', 'zombie', 'grinch', 'deranged'
    ]
    return f'the {honorifics[random.randrange(0, len(honorifics))]}'


def check_all_players_done():
    """Update path and then give to narrator."""
    global PLAYERS
    print('waiting for responses')

    total_players = len(PLAYERS)
    responses = 0

    for player in PLAYERS.values():
        if player.has_responded:
            responses += 1

    print(f'responses: {responses}')

    if responses == total_players:
        print('All players responded')
        for player in PLAYERS.values():
            player.has_responded = False
        advance_story()
