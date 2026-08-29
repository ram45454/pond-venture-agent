import re
from typing import Tuple

class SignalClassifier:
    def __init__(self):
        self.primary_intent = re.compile(
            r"\b(got into yc|accepted (to|into) yc|accepted (to|into) ycombinator|we're in yc|joined speedrun|accepted to speedrun)\b",
            re.IGNORECASE
        )
        self.secondary_context = re.compile(
            r"\b(moving to sf|yc s26|yc w26|speedrun cohort|demo day|building in public)\b",
            re.IGNORECASE
        )
        self.negative_patterns = re.compile(
            r"\b(how to get into|apply to|techcrunch|venture capital|vc firm|newsletter)\b",
            re.IGNORECASE
        )

    def classify_social_post(self, text: str) -> Tuple[str, float]:
        score = 0.0
        
        if self.primary_intent.search(text):
            score += 0.5
        if self.secondary_context.search(text):
            score += 0.3
        if self.negative_patterns.search(text):
            score -= 0.4

        if score >= 0.5:
            return "EARLY_SIGNAL", score
        return "NOISE", score

    @staticmethod
    def parse_batch_info(text: str) -> str:
        match = re.search(r"\b(YC\s*[SW]\d{2}|Cohort\s*\d{3})\b", text, re.IGNORECASE)
        if match:
            return match.group(0).upper()
        return "YC S26"
