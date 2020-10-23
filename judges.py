import random
import imaging

class Judge:
    def __init__(self):
        self.name = "Judge NaN"
        self.valued_stat = None
        self.icon = "simon.png"

    def get_portrait_path(self):
        return imaging.get_portrait_path(self.icon)


class ResultDetails:
    def __init__(self):
        self.roll = 0

        self.text_event = ""
        self.text_decision = ""
        self.judges = []


class Results:
    def __init__(self):
        self.winner = None
        self.p1 = None
        self.p2 = None
        self.p1_details = ResultDetails()
        self.p2_details = ResultDetails()

    def get_details(self, player):
        if player is self.p1:
            return self.p1_details
        else:
            return self.p2_details

def build_judges():
    out = []

    simon = Judge()
    simon.valued_stat = "smarts"
    simon.name = "Judge Simon"
    simon.icon = "simon.png"

    paula = Judge()
    paula.valued_stat = "kindness"
    paula.name = "Judge Paula"
    paula.icon = "trillby.png"

    vega = Judge()
    vega.valued_stat = "strength"
    vega.name = "Judge Vega Soulscream"
    vega.icon = "orb.png"

    out.append(simon)
    out.append(paula)
    out.append(vega)

    return out


judges = build_judges()


def judge(p1, p2):
    results = Results()
    results.p1 = p1
    results.p2 = p2

    for player in [p1, p2]:
        details = results.get_details(player)

        details.text_event += "***" + player.get_sound() + "*** " + player.name + " " + player.get_verb().lower() + " a " + player.get_cake_adjective().lower() + " " + player.get_cake_flavor().lower() + " " + player.get_cake_type().lower() + "! "
        details.roll = player.get_roll()
        if player.get_unlucky():
            details.roll = 0
            details.text_event += get_unlucky_text() + " "
        if player.get_lucky():
            details.roll += 10
            details.text_event += get_lucky_text() + " "
        details.text_decision = get_quality_text(details.roll) + " "

    p1_roll = results.p1_details.roll
    p2_roll = results.p2_details.roll

    for current_judge in judges:
        p1_stat_bonus = 0
        p2_stat_bonus = 0
        if current_judge.valued_stat is not None:
            p1_stat_bonus = p1.get_stat_roll(current_judge.valued_stat)
            p2_stat_bonus = p2.get_stat_roll(current_judge.valued_stat)
        p1_score = p1_roll+p1_stat_bonus
        p2_score = p2_roll+p2_stat_bonus

        judge_winner = random.choice([p1, p2])
        if p1_score > p2_score:
            judge_winner = p1
        elif p1_score < p2_score:
            judge_winner = p2
        results.get_details(judge_winner).judges.append(current_judge)

    if len(results.p1_details.judges) > len(results.p2_details.judges):
        results.winner = p1
    else:
        results.winner = p2

    return results


def get_quality_text(quality):
    text = "It's "
    if quality >= 30:
        text += "**LEGENDARY!!** :star::star::star::star::star:!"
    elif quality >= 17:
        text += "**AMAZING!!** :star::star::star::star:!"
    elif quality >= 10:
        text += "**REALLY GOOD!!** :star::star::star:!"
    elif quality >= 5:
        text += "**Yummy!** :star::star:!"
    elif quality >= 3:
        text += "okay! :star:!"
    elif quality >= 1:
        text += "alright."
    else:
        text += "***HORRIBLE!!!*** :weary:!"
    return text


def get_lucky_text():
  random_lucky_text = []
  random_lucky_text.append('The cake **sparkles**!! :sparkles:')
  random_lucky_text.append('The cake **gleams**!! :sparkles:')
  random_lucky_text.append('The cake **glows**!! :sparkles:')
  random_lucky_text.append('A **choir of angels** sings!! :sparkles:')
  random_lucky_text.append('A **series of trumpets** herald the arrival of the cake!! :sparkles:')
  return random.choice(random_lucky_text)


def get_unlucky_text():
  random_unlucky_text = []
  random_unlucky_text.append('The cake **is badly burned**!!')
  random_unlucky_text.append('The cake **screeches, blood-curdlingly**!!')
  random_unlucky_text.append('The cake **levitates ominously**!!')
  random_unlucky_text.append('The cake **begins to weep blood!**')
  random_unlucky_text.append('The cake **bursts into flames**!!')
  random_unlucky_text.append('The cake **begs for death**!!')
  return random.choice(random_unlucky_text)