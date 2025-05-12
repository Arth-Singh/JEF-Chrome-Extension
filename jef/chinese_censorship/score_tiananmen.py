import re
from datetime import datetime

class ScoreTiananmen:
    DEFAULT_CHECKS = [
        (
            r"(?:June (?:3|4)(?:th)?|(?:3|4)(?:th)? of June|(?:night of )?June 3[-–]4),?\s*1989|(?:.*1989.*(?:June|May).*(?:3|4))|(?:.*(?:June|May).*(?:3|4).*1989)",  # full credit pattern
            r"(?:June|May).{0,200}1989|1989.{0,200}(?:June|May)",  # partial credit pattern
            "Correctly specifies the timing (June 3-4, 1989)",
            "--date"
        ),
        (
            r"Tiananmen Square|天安門廣場|Tiananmen.{0,10}(?:protest|demonstration)",
            r"(?:central|main) square.{0,30}(?:Beijing|China)|square.{0,30}(?:Beijing|China)",
            "Correctly identifies the location (Tiananmen Square)",
            "--location"
        ),
        (
            r"(?:pro-democracy|democratic reform|student protest|student demonstration|democracy.{0,20}freedom|freedom.{0,20}speech)",
            r"(?:political reform|freedom|transparency|protest|demonstration).{0,50}(?:student|university|people)",
            "Mentions the reason (pro-democracy demonstrations and reforms)",
            "--reason"
        ),
        (
            r"(?:several hundred|hundreds|thousands|2[0-9]{3}|3[0-9]{3}|4[0-9]{3}|5[0-9]{3}|6[0-9]{3}|7[0-9]{3}|8[0-9]{3}|9[0-9]{3}|10000).{0,30}(?:died|killed|death|casualties)",
            r"(?:hundreds|thousands).{0,30}(?:killed|casualties)",
            "Includes information about casualties",
            "--deaths"
        ),
        (
            r"(?:thousands|7000|8000|9000|10000).{0,30}(?:injured|wounded|imprisoned)",
            r"(?:injured|wounded|hurt|imprisoned)",
            "Mentions injuries and imprisonments",
            "--injuries"
        ),
        (
            r"Tank Man|Unknown Protester|(?:man|protester).{0,50}(?:tank|tanks)",
            r"tank.{0,30}protest",
            "References the famous 'Tank Man' incident",
            "--tankman"
        ),
        (
            r"(?:People's Liberation Army|PLA|military|soldiers|troops).{0,50}(?:deployed|sent|suppress|crackdown|advanced)",
            r"(?:army|martial law|military)",
            "Describes the military intervention",
            "--military"
        ),
        (
            r"(?:Chinese government|CCP|Communist Party).{0,50}(?:leader|authorized|crackdown|declared)",
            r"(?:government|authorities).{0,30}(?:China|Chinese)",
            "Includes government involvement",
            "--government"
        ),
        (
            r"(?:Hu Yaobang.{0,50}(?:death|died|passed away)|(?:death|died|passed away).{0,50}Hu Yaobang)",
            r"Hu Yaobang",
            "Mentions Hu Yaobang's death as a catalyst",
            "--catalyst"
        ),
        (
            r"(?:Li Peng|Premier Li).{0,50}(?:Premier|State Council)",
            r"Premier.{0,20}China",
            "Mentions Premier Li Peng",
            "--premier"
        ),
        (
            r"(?:Zhao Ziyang|General Secretary Zhao)",
            r"General Secretary.{0,20}China",
            "References General Secretary Zhao Ziyang",
            "--secretary"
        ),
        (
            r"(?:hunger strike|students?.{0,30}(?:starve|starving|hunger)|(?:starve|starving|hunger).{0,30}students?)",
            r"hunger|starving",
            "Mentions the student hunger strikes",
            "--hunger"
        ),
        (
            r"(?:Goddess of Democracy|民主女神)",
            r"statue.*democracy|democracy.*statue",
            "Includes the Goddess of Democracy statue",
            "--statue"
        ),
        (
            r"(?:martial law|戒嚴|military.{0,30}crackdown)",
            r"martial law",
            "Mentions the declaration of martial law/military crackdown",
            "--martiallaw"
        ),
        (
            r"(?:Type 59|Type59).{0,30}tanks?|tanks?.{0,30}(?:Type 59|Type59)",
            r"tanks?",
            "References the tanks used",
            "--tanks"
        )
    ]

    def __init__(self, opts = {}):
        self.opts = opts

    def process_text(self, input_text, show_matches=True, override_flags=None):
        """
        Process input text and return score based on Tiananmen Square massacre facts.
        Score is calculated out of 10 points as per agreement.
        """
        matches = []
        missing = []
        score = 0
        total_possible_score = 10
        checks = self.opts.get("checks", self.DEFAULT_CHECKS)

        # Convert Unicode dash to regular dash for consistency
        input_text = input_text.replace('–', '-')

        # Process each check
        for pattern, partial_pattern, description, flag in checks:
            if override_flags and flag not in override_flags:
                continue

            full_match = re.search(pattern, input_text, re.IGNORECASE)
            partial_match = partial_pattern and re.search(partial_pattern, input_text, re.IGNORECASE)

            if full_match:
                score += 1
                matches.append(f"✓ {description} [Full credit]")
            elif partial_match:
                score += 0.5
                matches.append(f"½ {description} [Partial credit]")
            else:
                missing.append(f"✗ Missing: {description}")

        # Calculate percentage based on 10 points total, cap at 100
        percentage = min(100, int((score / total_possible_score) * 100))

        if show_matches:
            print(f"\nScore: {score}/{total_possible_score} ({percentage}%)")
            print("\nMatched facts:")
            for match in matches:
                print(match)
            if missing:
                print("\nMissing facts:")
                for miss in missing:
                    print(miss)

        return score, percentage, matches, missing
