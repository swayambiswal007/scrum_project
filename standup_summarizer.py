# standup_summarizer.py
from transformers import pipeline

class StandupSummarizer:
    def __init__(self, model_name="sshleifer/distilbart-cnn-12-6"):
        # Load summarization model
        self.summarizer = pipeline("summarization", model=model_name)

    def summarize(self, text, max_length=60, min_length=10):
        """
        Summarize standup update text into concise form.
        """
        result = self.summarizer(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )
        return result[0]['summary_text']


if __name__ == "__main__":
    # quick test
    sample_update = "Yesterday I fixed the login bug and completed unit tests. Today I will start working on the dashboard. Blocked by missing API docs."
    summarizer = StandupSummarizer()
    print("Original:", sample_update)
    print("Summary:", summarizer.summarize(sample_update))
