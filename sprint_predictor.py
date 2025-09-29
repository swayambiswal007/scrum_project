# sprint_predictor.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib  # for saving the trained model

class SprintPredictor:
    def __init__(self, model_path="sprint_model.pkl"):
        self.model_path = model_path
        self.model = None

    def train(self, csv_path):
        """
        Train regression model using sprint data.
        """
        data = pd.read_csv(csv_path)

        X = data[["team_size", "sprint_duration_days", 
                  "avg_story_points_per_member", "bugs_last_sprint"]]
        y = data["story_points_completed"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        preds = self.model.predict(X_test)

        print("📊 Training Report:")
        print("MAE:", mean_absolute_error(y_test, preds))
        print("R²:", r2_score(y_test, preds))

        joblib.dump(self.model, self.model_path)
        print(f"✅ Model saved to {self.model_path}")

    def load_model(self):
        self.model = joblib.load(self.model_path)

    def predict(self, team_size, sprint_duration_days, avg_story_points_per_member, bugs_last_sprint):
        """
        Predict story points for next sprint.
        """
        if self.model is None:
            self.load_model()

        input_data = [[team_size, sprint_duration_days, avg_story_points_per_member, bugs_last_sprint]]
        prediction = self.model.predict(input_data)[0]
        return prediction


if __name__ == "__main__":
    predictor = SprintPredictor()
    
    # Train model on CSV
    predictor.train("sample_data/sprint_data.csv")
    
    # Test prediction
    pred = predictor.predict(team_size=6, sprint_duration_days=14,
                             avg_story_points_per_member=7.2, bugs_last_sprint=9)
    print("Predicted story points:", pred)
