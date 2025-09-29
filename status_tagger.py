# status_tagger.py

import re

class StatusTagger:
    def __init__(self):
        # Define keyword lists for each category
        self.done_keywords = ["finished", "completed", "done", "yesterday"]
        self.next_keywords = ["today", "plan", "will start", "next"]
        self.blocked_keywords = ["blocked", "stuck", "waiting", "issue"]

    def tag_status(self, text):
        """
        Given a standup update, return status tags (done, next, blocked).
        """
        tags = []

        text_lower = text.lower()

        if any(word in text_lower for word in self.done_keywords):
            tags.append("done")

        if any(word in text_lower for word in self.next_keywords):
            tags.append("next")

        if any(word in text_lower for word in self.blocked_keywords):
            tags.append("blocked")

        return tags


if __name__ == "__main__":
    # quick test
    tagger = StatusTagger()
    sample_update = "Yesterday I finished login bug fix. Today I will start dashboard. Blocked by missing API docs."
    print("Update:", sample_update)
    print("Tags:", tagger.tag_status(sample_update))
