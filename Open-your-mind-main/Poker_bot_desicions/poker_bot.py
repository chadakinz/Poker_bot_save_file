#This is poker_bots control center, this is where he will execute his instructions
from Poker_bot_desicions.Equity import equity
from Poker_bot_desicions.Villain import Villain
from Poker_bot_desicions.handRankingspt2 import pre_flop_rating
class PokerBot:
    def __init__(self, chips):
        self.position = None
        self.cards = []
        self.table = []
        self.chips = chips
        self.positon = None
        self.bigBlind = False
        self.raise_total = 0
    #This mehtod currently only works for a HUNL style game
    def action(self,  pot_size, bet_size, game_state, table, position, Raise = False, All_In = False):
        if type(position[0]) == PokerBot:
            player_1 = Villain('Player1')
            player_1.position = 'LP'
        else:
            player_1 = Villain('Player1')
            player_1.position = 'EP'
        total_equity = 1

        #print(f'POKER BOT RECIEVED INFO: TABLE: {table} BET_SIZE: {bet_size}: CARDS: {self.cards}')
        pot_odds = bet_size / pot_size


        if game_state != 'Pre-Flop':

        #Players will be a list of all the players in the game

            equity_against_player = equity(self.cards, player_1.preflop_hand_distribution(), table)
            total_equity *= equity_against_player
            #print(f'Bot Equity: {total_equity}')
            #print(f'Pot Odds: {pot_odds}')

        #Poker Bot checks its expected value, if positive, then call, if negative, then fold
        # Expected value if check / call
            opponent_equity = 1 - total_equity
            win = total_equity * (pot_size + bet_size)
            lose = -((1 - total_equity) * (bet_size))

            expected_value = win + lose

            # Expected value if we raise
            win_fold = total_equity * (pot_size + bet_size)
            win_call = (total_equity ** 2) * (pot_size + bet_size + self.chips)
            lose_call = -((1 - total_equity) ** 2) * (self.chips)
            expected_value_raise = win_fold + win_call + lose_call
            if All_In == True:
                if expected_value > 0 or expected_value_raise > 0:
                    return 'Call'
                else:
                    return 'Fold'


            if expected_value_raise > expected_value and expected_value_raise > 0 and All_In == False:

                closest_raise_amount = {}
                for i in range(4000):
                    closest_raise_amount[abs(opponent_equity - (i/pot_size))] = i

                self.raise_amount = closest_raise_amount[min(closest_raise_amount.keys())]
                if self.raise_amount < bet_size * 2:
                    self.raise_amount = (bet_size * 2) - self.raise_total
                elif bet_size == 0 and self.raise_amount < 50:
                    self.raise_amount = 50

                if self.raise_amount >= self.chips:

                    return 'All_In'
                else:
                    self.raise_total += self.raise_amount
                    return 'Raise'

            elif (expected_value_raise < expected_value and expected_value > 0) or (expected_value_raise < expected_value and expected_value > 0):

                if Raise == True:
                    return 'Call'
                elif Raise == False:
                    return 'Check'

            elif expected_value_raise <= 0 and expected_value <= 0:
                if Raise == False:
                    return 'Check'
                elif Raise == True:
                    return 'Fold'

        else:
            return self.pre_flop_action(bet_size, Raise = Raise, All_In = All_In)
    #Method that is going to decide whether we play our pre flop cards based on their hand rankings + position + prior bets
    def pre_flop_action(self, bet_size, Raise = False, All_In = False):
        number_ranking = pre_flop_rating(self.cards)

        #High Range
        if number_ranking <= 42:
            #These are our all in cards, we can raise all the way to our max value of chips
            if number_ranking <= 8:

                #If we are first to act or our opponent checks, raise a smaller amount as to not scare our opponent off
                if bet_size == 100:
                    range_percentage = .20

                    self.raise_amount = round(250 + (self.chips * range_percentage)) - self.raise_total


                    if self.raise_amount >= self.chips:
                        return 'All_In'
                    self.raise_total += self.raise_amount
                    return 'Raise'

                #If our opponent raises, we are going to reraise based on a percentage of their raised amount
                elif bet_size > 100:
                    self.raise_amount = (2 * bet_size) - self.raise_total

                    if self.raise_amount >= self.chips:
                        return 'All_In'
                    self.raise_total += self.raise_amount

            else:
                if Raise == False or bet_size == 50:
                    range_percentage = .18 / abs(8 - number_ranking)

                    self.raise_amount = round(250 + (range_percentage * self.chips)) - self.raise_total
                    self.raise_total += self.raise_amount

                    if self.raise_amount >= self.chips:

                        return 'All_In'
                    else:
                        self.raise_total += self.raise_amount
                        return 'Raise'

                elif bet_size > 50 and Raise == True:

                    higher_range  =  self.chips * (.85 - (abs(9 - number_ranking) * .009090909))
                    lower_range = self.chips * (.45 - (abs(9 - number_ranking) * .009090909))

                    if bet_size <= higher_range and bet_size >= lower_range:
                        return 'Call'
                    elif bet_size <= lower_range:
                        for i in range(10):
                            Value = round(i * bet_size)
                            self.raise_amount = Value

                            if Value <= higher_range and Value >= lower_range:
                                if Value < 2 * bet_size:
                                    self.raise_amount = 2 * bet_size
                                    break
                                break
                            elif Value >= higher_range:
                                if Value < 2 * bet_size:
                                    self.raise_amount = 2 * bet_size
                                    break
                                #FIXME
                                self.raise_amount = round((i - 1) * bet_size)
                                break

                        self.raise_amount = self.raise_amount - self.raise_total


                        if self.raise_amount >= self.chips:

                            return 'All_In'
                        else:
                            self.raise_total += self.raise_amount
                            return 'Raise'
                    elif bet_size > higher_range:
                        return 'Fold'

        #Middle Range
        if number_ranking >= 43 and number_ranking <= 84:
            #If top of middle range, min-click + percentage
            range_percentage =  .08 / abs(42 - number_ranking)

            if (bet_size <= (250 + (range_percentage * self.chips)) )and Raise == True:
                return 'Call'
            elif (bet_size > (250 + (range_percentage * self.chips))) and Raise == True:
                return 'Fold'

            elif Raise == False:

                self.raise_amount = round(250 + (range_percentage * self.chips)) - self.raise_total
                if self.raise_amount >= self.chips:
                    return 'All_In'
                self.raise_total += self.raise_amount
                return 'Raise'


        #Low Range
        #if bet_size == Big Blind
        if number_ranking >= 85 and number_ranking <= 125:
            if bet_size == 50:
                return 'Call'
            elif Raise == False:
                return 'Check'
            else:
                return 'Fold'

        #Check/Fold Range
        if number_ranking >= 126 and number_ranking <= 169:
            if Raise == True:
                return 'Fold'
            else:
                return 'Check'






















