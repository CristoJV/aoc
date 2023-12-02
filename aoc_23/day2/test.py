import random
import unittest
from functools import reduce

from main import (
    count_cubes_in_bag,
    minimize_bag_contents,
    validate_bag_contents,
)


def generate_random_games(n_games, max_occurrences, bag_contents):
    """
    This function generates random games.

    Each game has a random number of occurrences. Each occurrence
    has a random number of colored cubes. Each cube has a random color and
    a random amount.

    The function returns a list of games, a list of occurrences for each game
    and a list of impossible games ids.

    Args:
        n_games: number of games to generate
        max_occurrences: maximum number of occurrences per game
        bag_contents: dictionary with the number of cubes per color in the bag

    Returns:
        games: list of games strings. Each game string has the following format:
            Game <game_id>: <occurrence_1>; <occurrence_2>; ...; <occurrence_n>
        games_occurrences: list of occurrences for each game
        impossible_games: list of impossible games ids
    """
    # Keep track of impossible games ids
    impossible_games = []

    # Generate random games
    games = []
    games_max_color = []

    # Keep track of the occurrences for each game
    games_occurrences = []

    for idx in range(n_games):
        # Note: the game_id is idx + 1
        game_id = idx + 1

        # Generate random number of occurrences per game
        n_occurrences = random.randint(1, max_occurrences)
        occurrences = []

        # Keep track of impossible occurrence
        impossible_occurrence = False

        occurrence_strings = []

        game_max_color = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }

        for occurrence_idx in range(n_occurrences):
            # Generate a base occurrence
            contents = {
                "red": random.randint(1, bag_contents["red"]),
                "green": random.randint(0, bag_contents["green"]),
                "blue": random.randint(0, bag_contents["blue"]),
            }

            # Choose a random color to be kept. Other colors
            # might be removed later by random choice
            color = random.choice(["red", "green", "blue"])

            # Randomly remove other colors
            temp_contents = contents.copy()
            for key in temp_contents.keys():
                if key != color:
                    if random.random() < 0.5:
                        contents.pop(key)

            # Randomly determine if the occurrence is impossible
            if random.random() < 0.5:
                color_choice = random.choice(list(contents.keys()))
                contents[color_choice] = bag_contents[color_choice] + 1
                impossible_occurrence = True

            # Keep track of the maximum amount of cubes per color
            if "red" in contents and contents["red"] > game_max_color["red"]:
                game_max_color["red"] = contents["red"]
            if (
                "green" in contents
                and contents["green"] > game_max_color["green"]
            ):
                game_max_color["green"] = contents["green"]
            if (
                "blue" in contents
                and contents["blue"] > game_max_color["blue"]
            ):
                game_max_color["blue"] = contents["blue"]

            # Generate occurrence string
            color_strings = []
            for key in contents.keys():
                color_strings.append(f"{contents[key]} {key}")
            occurrence_strings.append(", ".join(color_strings))

        # Keep track of impossible games
        if impossible_occurrence:
            impossible_games.append(game_id)

        # Generate game string
        game_string = f"Game {game_id}: "
        game_string += "; ".join(occurrence_strings)

        games_occurrences.append(occurrence_strings)
        games.append(game_string)
        games_max_color.append(game_max_color)

    return games, games_occurrences, impossible_games, games_max_color


class TestValidateBagContents(unittest.TestCase):
    """
    This test case is used to validate the validate_bag_contents function.

    It generates random games and check if the function returns the correct
    answer.

    The test game is run 1000 times.
    """

    def setUp(self) -> None:
        self.part = 1
        self.contents = {"red": 12, "green": 13, "blue": 14}
        self.n_games = 1000
        self.max_occurrences = 10

    def test_validate_bag_contents(self):
        """
        Tests that the validate_bag_contents function identifies either
        possible or impossible games.
        """
        (
            games,
            games_occurrences,
            impossible_games,
            _,
        ) = generate_random_games(
            self.n_games, self.max_occurrences, self.contents
        )

        lines = games.copy()
        for idx, game_occurrence in enumerate(games_occurrences):
            game_id = idx + 1
            if game_id in impossible_games:
                self.assertEqual(
                    False,
                    validate_bag_contents(game_occurrence, self.contents),
                    msg=f"\nMissing imposible game:\n Bag contents: {self.contents} \n {games[idx]}",
                )
            else:
                self.assertEqual(
                    True,
                    validate_bag_contents(game_occurrence, self.contents),
                    msg=f"\nMissing possible game:\n Bag contents: {self.contents} \n {games[idx]}",
                )

    def test_count_cubes_in_bag(self):
        """
        Tests that the sum of the possible games ids is correct.
        """
        games, games_occurrences, impossible_games, _ = generate_random_games(
            self.n_games, self.max_occurrences, self.contents
        )

        lines = games.copy()
        result = count_cubes_in_bag(lines, part=self.part)
        total = (len(games) * (len(games) + 1)) / 2
        answer = int(total - sum(impossible_games))

        self.assertEqual(result, answer)

    def test_minimize_bag_contents(self):
        """
        Test that the minimize_bag_contents function returns the correct
        answer.
        """
        (
            games,
            games_occurrences,
            impossible_games,
            games_max_color,
        ) = generate_random_games(
            self.n_games, self.max_occurrences, self.contents
        )
        lines = games.copy()
        for idx, game_occurrence in enumerate(lines):
            game_id = idx + 1
            result = minimize_bag_contents(games_occurrences[idx])
            self.assertEqual(
                result, games_max_color[idx], msg=f"\n{game_occurrence}"
            )

    def test_power_sum_bag_contents(self):
        """
        Test that the power sum of the possible games is correct.
        """
        self.part = 2
        (
            games,
            games_occurrences,
            impossible_games,
            games_max_color,
        ) = generate_random_games(
            self.n_games, self.max_occurrences, self.contents
        )
        lines = games.copy()
        result = count_cubes_in_bag(lines, part=self.part)
        answer = 0
        for game_max_color in games_max_color:
            answer += reduce(lambda x, y: x * y, game_max_color.values())
        self.assertEqual(result, answer)


if __name__ == "__main__":
    unittest.main()
