# # main.py
# import argparse
# import json

# from standup_summarizer import StandupSummarizer
# from status_tagger import StatusTagger
# from sprint_predictor import SprintPredictor
# import utils


# def run_summarization(input_file):
#     summarizer = StandupSummarizer()
#     tagger = StatusTagger()

#     with open(input_file, "r") as f:
#         standups = json.load(f)

#     for member, update in standups.items():
#         summary = summarizer.summarize(update)
#         tags = tagger.tag_status(update)

#         print(f"\n👤 {member}")
#         print("Original:", update)
#         print("Summary:", summary)
#         print("Tags:", tags)

#         # Save to logs
#         utils.log_standup(member, update, summary, tags)


# def run_prediction(csv_file, team_size, sprint_duration_days, avg_story_points_per_member, bugs_last_sprint):
#     predictor = SprintPredictor()
#     predictor.train(csv_file)

#     prediction = predictor.predict(
#         team_size=team_size,
#         sprint_duration_days=sprint_duration_days,
#         avg_story_points_per_member=avg_story_points_per_member,
#         bugs_last_sprint=bugs_last_sprint
#     )

#     print("\n📈 Predicted story points:", prediction)

#     # Save to logs
#     features = {
#         "team_size": team_size,
#         "sprint_duration_days": sprint_duration_days,
#         "avg_story_points_per_member": avg_story_points_per_member,
#         "bugs_last_sprint": bugs_last_sprint
#     }
#     utils.log_prediction(features, prediction)


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="AI Scrum Assistant")
#     subparsers = parser.add_subparsers(dest="command")

#     # Summarization
#     summarize_parser = subparsers.add_parser("summarize", help="Summarize standups")
#     summarize_parser.add_argument("--input", required=True, help="Path to standups JSON file")

#     # Prediction
#     predict_parser = subparsers.add_parser("predict", help="Predict next sprint story points")
#     predict_parser.add_argument("--sprint-csv", required=True, help="Path to sprint_data.csv")
#     predict_parser.add_argument("--team-size", type=int, required=True)
#     predict_parser.add_argument("--sprint-duration-days", type=int, required=True)
#     predict_parser.add_argument("--avg-story_points_per_member", type=float, required=True)
#     predict_parser.add_argument("--bugs-last-sprint", type=int, required=True)

#     # Run-all
#     runall_parser = subparsers.add_parser("run-all", help="Run summarization + prediction")
#     runall_parser.add_argument("--standups", required=True, help="Path to standups JSON file")
#     runall_parser.add_argument("--sprint-csv", required=True, help="Path to sprint_data.csv")
#     runall_parser.add_argument("--team-size", type=int, required=True)
#     runall_parser.add_argument("--sprint-duration-days", type=int, required=True)
#     runall_parser.add_argument("--avg-story_points_per_member", type=float, required=True)
#     runall_parser.add_argument("--bugs-last-sprint", type=int, required=True)

#     args = parser.parse_args()

#     if args.command == "summarize":
#         run_summarization(args.input)

#     elif args.command == "predict":
#         run_prediction(
#             args.sprint_csv,
#             args.team_size,
#             args.sprint_duration_days,
#             args.avg_story_points_per_member,
#             args.bugs_last_sprint
#         )

#     elif args.command == "run-all":
#         run_summarization(args.standups)
#         run_prediction(
#             args.sprint_csv,
#             args.team_size,
#             args.sprint_duration_days,
#             args.avg_story_points_per_member,
#             args.bugs_last_sprint
#         )

#     else:
#         parser.print_help()
from flask import Flask, render_template, request
from sprint_predictor import SprintPredictor
import os

app = Flask(__name__)
MODEL_PATH = "sprint_model.pkl"

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None

    if request.method == "POST":
        team_size = int(request.form["team_size"])
        sprint_duration_days = int(request.form["sprint_duration_days"])
        avg_story_points_per_member = float(request.form["avg_story_points_per_member"])
        bugs_last_sprint = int(request.form["bugs_last_sprint"])

        predictor = SprintPredictor(model_path=MODEL_PATH)

        # Train model if not already saved
        if not os.path.exists(MODEL_PATH):
            predictor.train("data/sprint_data.csv")

        prediction = predictor.predict(
            team_size,
            sprint_duration_days,
            avg_story_points_per_member,
            bugs_last_sprint
        )

    return render_template("index.html", prediction=prediction)


if __name__ == "__main__":
    app.run()

