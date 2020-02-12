from random import shuffle


# class constructor
class Card:
    def __init__(self, name, number, suit):
        self.name = name
        self.number = number
        self.suit = suit


# class with methods
class NewCards:

    cardArr = []   # array with class Card instances
    allCards = []  # final array

    # this method fill array with cards; there are two types of cards: board cards & deck cards
    @classmethod
    def define_cards(cls):

        for i in range(13):

            for j in range(4):

                numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1]

                names = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]

                suits = ["Diamonds", "Hearts", "Spades", "Clubs"]

                cls.cardArr.append(Card(names[i], numbers[i], suits[j]))

        shuffle(cls.cardArr)

        for i in range(len(cls.cardArr)):

            lines = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7]

            move = [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]

            if i < 28:

                cls.cardArr[i].line = lines[i]  # line on board

                cls.cardArr[i].move = move[i]   # the first cards of each line

                cls.cardArr[i].type = "board"

                cls.cardArr[i].removed = False

            elif i == 51:

                cls.cardArr[i].type = "deck"

                cls.cardArr[i].blocked = False

            else:

                cls.cardArr[i].type = "deck"

                cls.cardArr[i].blocked = True

            cls.cardArr[i].id = i

            cls.allCards.append(cls.cardArr[i])

        return cls.allCards

    # this method places cards on board
    @staticmethod
    def draw_cards(cards):

        print("\nDeck [{}]: {}".format(len(cards) - 28, "[ id: {}, value: {} ]".format(cards[-1].id, cards[-1].name)))

        for i in cards:

            if i.type == "board":

                is_blocked = any(i.id + i.line == x.id or i.id + i.line + 1 == x.id for x in cards if x.type == "board")  # is parent cards is exist

                if is_blocked:

                    i.blocked = True

                else:

                    i.blocked = False

                if i.move:  # new line

                    if i.removed:  # card already used

                        print("\nLine {}".format(i.line), "    ", end="   ")

                    elif i.blocked:  # card w/o value

                        print("\nLine {}: ".format(i.line), "[ id: {}, value: {} ]".format(i.id, "X"), end="   ")

                    else:

                        print("\nLine {}: ".format(i.line), "[ id: {}, value: {} ]".format(i.id, i.name), end="   ")

                else:

                    if i.removed:

                        print("    ", end="   ")

                    elif i.blocked:

                        print("[ id: {}, value: {} ]".format(i.id, "X"), end="   ")

                    else:

                        print("[ id: {}, value: {} ]".format(i.id, i.name), end="   ")

    # this method processed commands from console
    @classmethod
    def start(cls, cards):

        do = input("\n\nEnter command: ").split(" ")

        if do[0] == "add":

            do.remove("add")

            if len(do) > 2:

                print("Error!")

                Main.draw_cards(cards)

                Main.start(cards)

            summed = 0

            for i in range(len(do)):

                item = None

                for x in cards:

                    if x.id == int(do[i]):

                        item = x

                        break

                if item and not item.blocked:

                    summed += item.number

                else:

                    print("Seems like you trying to add blocked / unexisted cards: ", cards[int(do[i])].__dict__)

            if summed == 13:

                print("Removed")

                for i in range(len(do)):

                    if cards[int(do[i])].type == "board":

                        cards[int(do[i])].number = 999

                        cards[int(do[i])].name = "   "

                        cards[int(do[i])].id = 999

                        cards[int(do[i])].removed = True

                    else:

                        del cards[-1]

                        cards[-1].blocked = False

            else:

                print("Dickhead!")

        elif do[0] == "next":

            cards[-1].blocked = True

            for i in range(len(cards) - 1, 28, -1):

                cards[i], cards[i - 1] = cards[i - 1], cards[i]

            cards[-1].blocked = False

        elif do[0] == "info":

            Main.show_info()

        elif do[0] == "rules":

            Main.show_rules()

        else:

            print("Unknown command!")

            Main.draw_cards(cards)

            Main.start(cards)


# class with methods for process running
class Main(NewCards):

    # this method prints rules
    @staticmethod
    def show_rules():

        print("\nRules:\n\nYou need to add cards to make number 13, when all cards are removed - you will win.")

    # this method prints info
    @staticmethod
    def show_info():

        print("\nCommand list: \n\nadd [smth] / add [smth] [smth] - add card to card;\nnext - show next deck card;\nrules - show rules;\ninfo - show this message again.")

    # this methods runs game loop
    @staticmethod
    def game():

        Main.show_rules()
        Main.show_info()

        card = NewCards()

        cards = card.define_cards()

        while True:

            Main.draw_cards(cards)

            Main.start(cards)

            if cards[0].removed:

                print("You won.")

                break


main = Main()

main.game()
