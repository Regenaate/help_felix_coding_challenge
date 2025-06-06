from typing import List
import os
import sys
import time


class StoryNode:
    def __init__(self, value, question, options: List["StoryNode"] = [], trigger=None):
        self.trigger = trigger  # This determines what cuases this prompt to come out
        self.value = value  # The text of the story node, the stuff that comes before the options are presented
        self.question = question  # The question that is asked to the player, which is usually the same as the value
        self.options = options  # The options that the player can choose from, which are also story nodes


# 1. "Help him find a girlfiend"

# some class or function helps

# Girlfriend?

# (trigger) - "Help him find a girlfiend"
# (value) - You want to help him get a girlfriend? Alright. So Felix tells you he matched with 3 different women on a dating site. But he can't decide which one he wants to ask out. He doesn't know anything about the women besides their names, but he wants you decide which one he should try first.
# (question) - Which woman will you suggest for Felix to take on a date?
# (Options):
# 1. Stacy (Stacy is a cold gold digger, so you'll have to get good at your life insurance job first. Felix won't be the happiest with her, but it will achieve his goal of companionship)
# 2. Samantha (Samantha will only work if Felix hasn't overcome his paranoia, because she has paranoia too. She is…kind of a psycho and can help you achieve your life insurance goal by instilling fear into your potential clients. In the end, she'll admit that she's actually a man, but you'll outgrow it and live happily ever after.)
# 3. Lizarda (so Lizarda will only work if Felix overcomes his paranoia first. Otherwise, you'll lose. But if he does, she will help him out with selling life insurance with her…soft skills 😂)


# Story value


class Player:
    def __init__(self):
        self.girlfriend = False
        self.job = False
        self.paranoia = False

    def check_goals(self):
        return self.girlfriend and self.job and self.paranoia


class FelixGame:
    def __init__(self, story: StoryNode, felix: Player):
        self.story = story
        self.felix = felix

    def start_game(self):
        self.slow_print(
            "So you're a therapist, and your client (Felix) wants your help on how to achieve his goals. Felix has 3 goals, and you must help him achieve each of them."
        )
        input("Enter to continue...")  # waits for user input
        os.system("clear")  # clears the terminal on Mac/Linux
        self.slow_print(
            "His goals are simple. He wants to get a girlfriend for support & companionship. He wants to get better at his job selling life insurance so he can earn more cash, and he wants to overcome his paranoia of believing that some people are secretly shapeshifting reptilians that are currently plotting for humanity's demise."
        )
        self.play_game()

    def play_game(self):
        current_node = self.story
        while not self.felix.check_goals():
            self.slow_print(current_node.value)
            self.slow_print(current_node.question)
            self.print_options(current_node.options)
            choice = input("Choose an option: ")
            self.handle_choice(choice, current_node)
        self.slow_print("Congratulations! You have helped Felix achieve all his goals!")

    def print_options(self, options: List[StoryNode]):
        for i, option in enumerate(options):
            print(f"{i + 1}. {option.value}")

    def handle_choice(self, choice: int, current_node: StoryNode):
        if choice.isdigit() and 1 <= int(choice) <= len(current_node.options):
            current_node = current_node.options[int(choice) - 1]
            if current_node.trigger:
                current_node.trigger(
                    self.felix
                )  # Call the trigger function if it exists
                current_node = self.story
        else:
            self.slow_print("Invalid choice, please try again.")

    def slow_print(self, text):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            # if char == ".":
            #     time.sleep(0.8)
            # elif char == ",":
            #     time.sleep(0.3)
            # else:
            #     time.sleep(0.05)  # Adjust the delay (in seconds) as needed
        print()  # Add a newline at the end


girlfriend_options = [
    StoryNode(
        "Stacy",
        "Stacy is a cold gold digger, so you'll have to get good at your life insurance job first. Felix won't be the happiest with her, but it will achieve his goal of companionship.",
        [],
        trigger=lambda player: setattr(player, "girlfriend", True),
    ),
    StoryNode(
        "Samantha",
        "Samantha will only work if Felix hasn't overcome his paranoia, because she has paranoia too. She is…kind of a psycho and can help you achieve your life insurance goal by instilling fear into your potential clients. In the end, she'll admit that she's actually",
        [],
        trigger=lambda player: setattr(player, "girlfriend", True),
    ),
    StoryNode(
        "Lizarda",
        "Lizarda will only work if Felix overcomes his paranoia first. Otherwise, you'll lose. But if he does, she will help him out with selling life insurance with her…soft skills 😂",
        [],
        trigger=lambda player: setattr(player, "girlfriend", True),
    ),
]

begning_options = [
    StoryNode(
        "Help him get a girlfriend",
        "Which girlfriend do you choose?",
        girlfriend_options,
    ),
    StoryNode(
        "Help him improve at his job",
        "Which job do you choose?",
        [],
        trigger=lambda player: setattr(player, "job", True),
    ),
    StoryNode(
        "Help him overcome his reptilian paranoia",
        "Which fear do you want to overcome?",
        [],
        trigger=lambda player: setattr(player, "paranoia", True),
    ),
]

story = StoryNode(
    "", "So which of Felix's goals will you help him out with first?", begning_options
)

game = FelixGame(story, Player())

game.start_game()
