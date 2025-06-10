import random
from typing import List
import os
import sys
import time
import termios
import tty
import select

class Player:
    def __init__(self):
        self.girlfriend = None
        self.good_at_job = False
        self.overcame_paranoia = False
        self.nathan_lost = False
        self.nathan_intrigued = False
        self.the_robinsons_lost = False
        self.alice_and_cooper_lost = False
        self.reaper_costume_on = False
        self.buisness_suit_on = False
        self.polo_and_khakis_on = False
        self.dumped_by_stacy = False
        self.dumped_by_lizarda = False

    def check_goals(self):
        return self.girlfriend and self.good_at_job and self.overcame_paranoia

class StoryNode:
    def __init__(self, trigger, value, question, options, effect):
        self.trigger = trigger  # This determines what cuases this prompt to come out
        self.value = value  # The text of the story node, the stuff that comes before the options are presented
        self.question = question  # The question that is asked to the player, which is usually the same as the value
        self.options = options  # The options that the player can choose from, which are also story nodes
        self.effect = effect # Optional effect to apply when this node is reached

class StoryMaster:
    def __init__(self):
        self.story = self.collect_story()

    @staticmethod
    def collect_story():
        story_nodes = []
        with open("three-problems.txt", "r") as f:
            content = f.read().strip()
            node_blocks = content.split("\n\n")  # Split by empty lines

            for block in node_blocks:
                lines = [line.strip() for line in block.split("\n") if line.strip()]
                if len(lines) < 5:
                    continue  # Not enough lines for a valid node

                trigger = lines[0]
                value = lines[1]
                question = lines[2]

                # Options: lines starting with a number
                options = []
                effect = ""
                for line in lines[3:]:
                    if line and line[0].isdigit():
                        # Remove the leading number and possible dot/space
                        option_text = line.lstrip("0123456789. ").strip()
                        options.append(option_text)
                    else:
                        effect = line  # Last non-option line is effect

                # Create the StoryNode (options as strings, not StoryNodes)
                node = StoryNode(trigger, value, question, options, effect)
                story_nodes.append(node)

        # Sort the story_nodes array by trigger before returning
        story_nodes.sort(key=lambda node: node.trigger)

        return story_nodes
    
    def get_next_story_node(self, trigger_string):
        # Binary search for the StoryNode with the matching trigger
        left, right = 0, len(self.story) - 1
        while left <= right:
            mid = (left + right) // 2
            mid_trigger = self.story[mid].trigger
            if mid_trigger == trigger_string:
                return self.story[mid]
            elif mid_trigger < trigger_string:
                left = mid + 1
            else:
                right = mid - 1
        print(f"Trigger '{trigger_string}' not found in story nodes.")
        return None  # Not found

class FelixGame:
    def __init__(self, starting_node: StoryNode, felix: Player, story_master: StoryMaster):
        self.story_master = StoryMaster()
        self.felix = felix
        self.game_over = False
        self.current_node = starting_node

    def start_game(self):
        self.slow_print(
            "So you're a therapist, and your client (Felix) wants your help on how to achieve his goals. Felix has 3 goals, and you must help him achieve each of them."
        )
        input("Enter to continue...")  # waits for user input
        os.system("clear")  # clears the terminal on Mac/Linux
        self.play_game()

    def play_game(self):
        current_node = self.current_node
        while not self.felix.check_goals() and not self.game_over:
            os.system("clear")  # clears the terminal on Mac/Linux
            self.apply_effect(current_node.effect)

            self.slow_print_prompt(
                current_node.value, current_node.question, current_node.options
            )
            if(self.game_over): break

            # Input validation loop
            while True:
                option_number_chosen = input("Choose an option: ").strip()
                if option_number_chosen.isdigit():
                    option_index = int(option_number_chosen) - 1
                    if 0 <= option_index < len(current_node.options):
                        break
                print("Invalid input. Please enter a valid option number.")
            choice = current_node.options[int(option_number_chosen) - 1] if option_number_chosen.isdigit() and 1 <= int(option_number_chosen) <= len(current_node.options) else None
            next_node = self.story_master.get_next_story_node(choice.strip())
            next_node = self.apply_alterations(next_node)
            current_node = next_node

        if self.felix.check_goals():
            self.slow_print(
                "Congratulations! You have helped Felix achieve all his goals!"
            )
            final_story_node = None
            if self.felix.girlfriend == "Stacy":
                final_story_node = self.story_master.get_next_story_node("End with Stacy")
            elif self.felix.girlfriend == "Samantha":
                final_story_node = self.story_master.get_next_story_node("End with Samantha")
            elif self.felix.girlfriend == "Lizarda":
                final_story_node = self.story_master.get_next_story_node("End with Lizarda")
            elif self.felix.girlfriend == "Nathan?":
                final_story_node = self.story_master.get_next_story_node("End with Nathan")
            self.slow_print(final_story_node.value)
            self.slow_print(final_story_node.question)
        else:
            self.slow_print("GAME OVER!\nYou did not help Felix achieve all his goals.")
        sys.exit(0)

    def print_options(self, options):
        for i, option in enumerate(options):
            print(f"{i+1}. {option}")
    
    def apply_effect(self, effect):
        if effect == "none":
            return
        if effect == "lose":
            self.game_over = True
            return
        
        if effect == "Girlfriend Get (Stacy)":
            self.felix.girlfriend = "Stacy"
        if effect == "Dumped by Stacy":
            self.felix.dumped_by_stacy = True
        elif effect == "Girlfriend Get (Samantha)":
            self.felix.girlfriend = "Samantha"
        if effect == "Girlfriend Get (Lizarda)":
            self.felix.girlfriend = "Lizarda"
        elif effect == "Dumped by Lizarda":
            self.felix.dumped_by_lizarda = True
        if effect == "Boyfriend Get (Nathan)":
            self.felix.girlfriend = "Nathan?"
        if effect == "Reaper Costume On":
            self.felix.reaper_costume_on = True
        if effect == "Business Suit On":
            self.felix.buisness_suit_on = True
        if effect == "Polo & Khakis On":
            self.felix.polo_and_khakis_on = True
        if effect == "Reaper Costume Off":
            self.felix.reaper_costume_on = False
        if effect == "Business Suit Off":
            self.felix.buisness_suit_on = False
        if effect == "Polo & Khakis Off":
            self.felix.polo_and_khakis_on = False

        if effect == "Nathan lost as potential customer":
            self.felix.nathan_lost = True
        elif effect == "Nathan lost as potential customer, but he is intrigued":
            self.felix.nathan_lost = True
            self.felix.nathan_intrigued = True
        elif effect == "Robinsons lost as potential customer":
            self.felix.the_robinsons_lost = True
        elif effect == "Alice & Cooper lost as potential customers":
            self.felix.alice_and_cooper_lost = True
        elif effect == "Felix becomes good at his job":
            self.felix.good_at_job = True
        
        if effect == "Reptile Fear Overcome":
            self.felix.overcame_paranoia = True
    
    def apply_alterations(self, story_node):
        if story_node.trigger == "Stacy (petite, 5'2, black-haired, light-brown-skinned woman, navy blue dress)" and self.felix.good_at_job:
            return self.story_master.get_next_story_node("Stacy Alt")
        elif story_node.trigger == "Lizarda (Slim, 5'7, Dark-Skin, Blonde, TNAL: Totally Not A Lizard)" and self.felix.overcame_paranoia:
            return self.story_master.get_next_story_node("Lizarda Alt")
        elif story_node.trigger == "Samantha (burly woman, 6'5, orange-hair, light-skinned, dresses like a biker)" and self.felix.overcame_paranoia:
            return self.story_master.get_next_story_node("Samantha Alt")
        elif story_node.trigger == "Re-select your attire":
            if self.felix.reaper_costume_on:
                return self.story_master.get_next_story_node("Re-select your attire (Reaper Costume)")
            elif self.felix.buisness_suit_on: 
                return self.story_master.get_next_story_node("Re-select your attire (Business Suit & Tie)")
            elif self.felix.polo_and_khakis_on:
                return self.story_master.get_next_story_node("Re-select your attire (Polo & Khakis)")
        elif story_node.trigger == "Back to goals":
            print(story_node.options)
            if self.felix.girlfriend:
                try:
                    story_node.options.remove('Help him get a girlfriend')
                except ValueError:
                    pass
            if self.felix.good_at_job:
                try:
                    story_node.options.remove('Help him improve at his job')
                except ValueError:
                    pass
            if self.felix.overcame_paranoia:
                try:
                    story_node.options.remove('Help him overcome his reptilian paranoia')
                except ValueError:
                    pass
        elif story_node.trigger == "Back to people to sell to":
            if self.felix.nathan_lost:
                try:
                    story_node.options.remove('Nathan (Single, no kids)')
                except ValueError:
                    pass
            if self.felix.the_robinsons_lost:
                try:
                    story_node.options.remove('The Robinsons (Family with 2 Kids)')
                except ValueError:
                    pass
            if self.felix.alice_and_cooper_lost:
                try:
                    story_node.options.remove('Alice & Cooper (Husband & Wife, no kids)')
                except ValueError:
                    pass
            if self.felix.nathan_lost and self.felix.the_robinsons_lost and self.felix.alice_and_cooper_lost:
                self.slow_print("You have lost all potential customers. You lose.")
                self.game_over = True
        elif (story_node.trigger == "Help him get a girlfriend") or (story_node.trigger == "Back to girlfriend choices"):
            if self.felix.nathan_intrigued:
                story_node.options.append('Nathan')
            if self.felix.dumped_by_lizarda:
                try:
                    story_node.options.remove("Lizarda (Slim, 5'7, Dark-Skin, Blonde, TNAL: Totally Not A Lizard)")
                except ValueError:
                    pass
            if self.felix.dumped_by_stacy:
                try:
                    story_node.options.remove("Stacy (petite, 5'2, black-haired, light-brown-skinned woman, navy blue dress)")
                except ValueError:
                    pass
        elif story_node.trigger == "Nathan (Single, no kids)":
            if self.felix.reaper_costume_on:
                return self.story_master.get_next_story_node("Nathan (Single, no kids, alt)")
        elif story_node.trigger == "The Robinsons (Family with 2 Kids)":
            if self.felix.overcame_paranoia:
                story_node = self.story_master.get_next_story_node("The Robinsons (Family with 2 Kids, alt)")
        if (story_node.trigger == "The Robinsons (Family with 2 Kids, alt)") or (story_node.trigger == "Attempt to mask Felix's fear (50% chance-of-success, success)"):
            if self.felix.girlfriend == "Lizarda":
                story_node.options.append('Summon Lizarda to help sell to the Robinsons')
        
        if (story_node.trigger == "Help him overcome his reptilian paranoia"):
            if self.felix.girlfriend == "Samantha":
                story_node.options.append('The Deadliest Person You know')
        if story_node.trigger == "Attempt new spell? (70% chance-of-success)":
            if self.activate_chance_roll(0.70):
                story_node = self.story_master.get_next_story_node("Attempt new spell? (success)")
            else:
                story_node = self.story_master.get_next_story_node("Attempt new spell? (fail)")
        if story_node.trigger == "Attempt to mask Felix's fear (60% chance-of-success)":
            if self.activate_chance_roll(0.60):
                story_node = self.story_master.get_next_story_node("Attempt to mask Felix's fear (success)")
            else:
                story_node = self.story_master.get_next_story_node("Attempt to mask Felix's fear (fail)")
        
        return story_node

    def slow_print(self, text, clear_screen=False):
        def is_input():
            return select.select([sys.stdin], [], [], 0)[0]

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        interrupted = False
        try:
            tty.setcbreak(fd)
            for char in text:
                if is_input():
                    interrupted = True
                    break
                sys.stdout.write(char)
                sys.stdout.flush()
                if char in ".!?":
                    time.sleep(0.8)
                elif char == ",":
                    time.sleep(0.3)
                else:
                    time.sleep(0.05)
            if interrupted:
                if clear_screen:
                    os.system("clear")
                print(text, end="", flush=True)
            print()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def slow_print_prompt(self, value, question, options):
        def is_input():
            return select.select([sys.stdin], [], [], 0)[0]

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        interrupted = False
        try:
            tty.setcbreak(fd)
            for char in value:
                if is_input():
                    interrupted = True
                    break
                sys.stdout.write(char)
                sys.stdout.flush()
                if char in ".!?":
                    time.sleep(0.8)
                elif char == ",":
                    time.sleep(0.3)
                else:
                    time.sleep(0.05)
            print()
            for char in question:
                if is_input() or interrupted:
                    interrupted = True
                    break
                sys.stdout.write(char)
                sys.stdout.flush()
                if char in ".!?":
                    time.sleep(0.8)
                elif char == ",":
                    time.sleep(0.3)
                else:
                    time.sleep(0.05)
            print()
            if(self.game_over):
                os.system("clear")
                print(value, flush=True)
                print(question, flush=True)
                return
            self.print_options(options)
            if interrupted:
                os.system("clear")
                print(value, flush=True)
                print(question, flush=True)
                self.print_options(options)

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def activate_chance_roll(self,chance):
        """Returns True if the chance roll is successful, False otherwise."""
        return random.random() < chance

story_master = StoryMaster()
starting_node = story_master.get_next_story_node("Start")
game = FelixGame(starting_node, Player(), story_master)

game.start_game()


