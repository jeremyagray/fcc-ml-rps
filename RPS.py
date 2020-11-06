import random
import re
import traceback

beat = {
    'R': 'P',
    'P': 'S',
    'S': 'R'
}


class Player:
    def __init__(self):
        self.opp_hist = []
        self.my_hist = []
        self.record = []

    def result(me, him):
        if ((me not in beat) or (him not in beat)):
            raise ValueError
        elif me == him:
            return 'D'
        elif me == beat[him]:
            return 'W'
        elif beat[me] == him:
            return 'L'
        else:
            raise ValueError


def player(prev_play, player_history=[], opponent_history=[]):

    def result(me, him):
        if ((me not in beat) or (him not in beat)):
            raise ValueError
        elif me == him:
            return 'D'
        elif me == beat[him]:
            return 'W'
        elif beat[me] == him:
            return 'L'
        else:
            raise ValueError

    def get_opponent():
        for line in traceback.format_stack():
            whole = ' '.join(line.strip().split('\n'))
            # print(whole)
            match = re.search(r'(quincy|abbey|kris|mrugesh)', whole)
            if match:
                return match.group(1)

    def get_winner(play):
        if play == 'R':
            return 'P'
        elif play == 'P':
            return 'S'
        elif play == 'S':
            return 'R'
        else:
            raise ValueError

    def mode(plays, num=0):
        if len(plays) == 0:
            return None

        counts = {}

        if num > 0:
            selection = plays[-num]
        else:
            selection = plays

        for play in selection:
            try:
                counts[play] += 1
            except KeyError:
                counts[play] = 1

        max = 0
        play = ''

        for (k, v) in counts.items():
            if v > max:
                max = v
                play = k

        return play

    def ars(me, him):
        choices = ['R', 'P', 'S']
        go_random = random.choice([0])

        if result(me, him) == 'D':
            return random.choice(choices)
        elif result(me, him) == 'W':
            if go_random:
                return random.choice(choices)
            else:
                return get_winner(him)
        elif result(me, him) == 'L':
            if go_random:
                return random.choice(choices)
            else:
                return get_winner(me)

    def beat_mode(plays):
        return get_winner(mode(plays))

    def play_mode(plays):
        return mode(plays)

    def rand():
        return random.choice(['R', 'P', 'S'])

    def rock():
        return 'R'

    def paper():
        return 'P'

    def scissor():
        return 'S'

    # quincy plays a sequence
    def anti_quincy(oh):
        qplays = []
        for play in oh:
            if play[0] == 'quincy':
                qplays.append(play)

        choices = ['R', 'R', 'P', 'P', 'S']
        choice = choices[(len(qplays) + 1) % 5]
        guess = beat[choice]
        # print('play:  {} q:  {} m:  {}'.format(len(qplays), choice, guess))
        return guess

    # kris plays to beat your last play
    def anti_kris(mh, oh):
        if len(mh) == 0:
            return random.choice(list(beat.keys()))
        else:
            if oh[-1][1] == mh[-1][1]:
                return random.choice(list(beat.keys()))
            else:
                return beat[beat[mh[-1][1]]]

    # mrugesh plays to beat my most common play in the last ten
    def anti_mrugesh(mh):
        if len(mh) == 0:
            return random.choice(list(beat.keys()))
        else:
            last = []
            for play in mh[-10:]:
                last.append(play[1])

            mode = max(set(last), key=last.count)

            if mode == '':
                mode = 'R'

            return beat[beat[mode]]

    # A second order Markov player that beats the second play of the most
    # played possible current two play sequence.
    def anti_abbey(mh):
        plays = {
            'RR': 0,
            'RP': 0,
            'RS': 0,
            'PR': 0,
            'PP': 0,
            'PS': 0,
            'SR': 0,
            'SP': 0,
            'SS': 0,
        }

        if len(mh) >= 2:
            last = None
            for i, play in enumerate(mh):
                if play[0] == 'abbey':
                    if last is None:
                        last = play[1]
                    else:
                        plays[last + play[1]] += 1
                        last = play[1]

            cplays = {
                play[1] + 'R': plays[play[1] + 'R'],
                play[1] + 'P': plays[play[1] + 'P'],
                play[1] + 'S': plays[play[1] + 'S']
            }

            return beat[beat[max(cplays, key=cplays.get)[-1:]]]
        else:
            return random.choice(list(beat.keys()))

    opponent = get_opponent()

    if prev_play != '':
        opponent_history.append((opponent, prev_play))

    if get_opponent() == 'quincy':
        guess = anti_quincy(opponent_history)
    elif get_opponent() == 'abbey':
        guess = anti_abbey(player_history)
    elif get_opponent() == 'kris':
        guess = anti_kris(player_history, opponent_history)
    elif get_opponent() == 'mrugesh':
        guess = anti_mrugesh(player_history)
    else:
        guess = rand()

    player_history.append((opponent, guess))

    return guess
