import random
import time
import joblib
from datetime import datetime
import pandas as pd 
# ----------------------
# Server Class
# ----------------------
class Server:
    def __init__(self, name, region):
        self.name = name
        self.region = region
        self.latency = random.randint(20, 100)     # ms
        self.cpu_load = random.uniform(0, 100)     # percentage
        self.packet_loss = random.uniform(0, 5)    # %
        self.jitter = random.uniform(0, 10)        # ms
        self.active_requests = 0                   # how many requests this server is handling

    def handle_request(self):
        self.active_requests += 1
        time.sleep(0.01)
        self.active_requests -= 1
        return f"Response from {self.name} in {self.region}"

    def get_metrics(self):
        self.latency = random.randint(20, 100)
        self.cpu_load = random.uniform(0, 100)
        self.packet_loss = random.uniform(0, 5)
        self.jitter = random.uniform(0, 10)
        return {
            "latency": self.latency,
            "cpu_load": self.cpu_load,
            "packet_loss": self.packet_loss,
            "jitter": self.jitter,
            "active_requests": self.active_requests
        }

# ----------------------
# Smart Router Class
# ----------------------
class SmartRouter:
    WEIGHTS = {
        "latency": 0.4,
        "cpu_load": 0.15,
        "packet_loss": 0.15,
        "jitter": 0.15,
        "active_requests": 0.05,
        "predicted_cpu_load": 0.10,  # AI prediction included
    }

    NORMALIZE = {
        "latency": 100,
        "cpu_load": 100,
        "packet_loss": 5,
        "jitter": 10,
        "active_requests": 10,
        "predicted_cpu_load": 100,
    }

    def __init__(self, servers, model_path):
        self.servers = servers
        self.model = joblib.load(model_path)

    def calculate_score(self, metrics):
        score = 0.0
        for metric in self.WEIGHTS:
            value = metrics.get(metric, 0)  # Use 0 if not present
            max_value = self.NORMALIZE[metric]
            normalized = min(value / max_value, 1.0)
            score += normalized * self.WEIGHTS[metric]
        return score

    def get_time_features(self):
        now = datetime.now()
        hour = now.hour
        dayofweek = now.weekday()
        minute = now.minute
        minute_of_day = hour * 60 + minute
        is_weekend = 1 if dayofweek >= 5 else 0
        return hour, dayofweek, minute_of_day, is_weekend

    def choose_best_server_with_scores(self):
        best_server = None
        best_score = float("inf")
        hour, dayofweek, _, _ = self.get_time_features()

        scores_data = []

        for s in self.servers:
            metrics = s.get_metrics()

            # Create the one-hot encoded features for the server names
            server_features = [0, 0, 0, 0]
            if s.name == "Server1": server_features = [1, 0, 0, 0]
            elif s.name == "Server2": server_features = [0, 1, 0, 0]
            elif s.name == "Server3": server_features = [0, 0, 1, 0]
            elif s.name == "Server4": server_features = [0, 0, 0, 1]
            
            # Build the feature list for prediction
            features_list = [[
                metrics["latency"], metrics["cpu_load"], metrics["packet_loss"],
                metrics["jitter"], metrics["active_requests"], hour, dayofweek,
                *server_features
            ]]

            feature_names = [
                "latency_ms", "cpu_load_percent", "packet_loss_percent", "jitter_ms",
                "active_requests", "hour", "dayofweek", "server_Server1", 
                "server_Server2", "server_Server3", "server_Server4"
            ]
            features_df = pd.DataFrame(features_list, columns=feature_names)
            predicted_cpu = self.model.predict(features_df)[0]
            
            metrics["predicted_cpu_load"] = predicted_cpu
            score = self.calculate_score(metrics)
            
            # Store data for the dashboard table
            row = metrics.copy()
            row['score'] = score
            row['server_name'] = s.name
            scores_data.append(row)
            
            if score < best_score:
                best_score = score
                best_server = s
        
        # Create a DataFrame from the collected scores
        scores_df = pd.DataFrame(scores_data).set_index('server_name')
        return best_server, scores_df

# ----------------------
# Simulation Example
# ----------------------
if __name__ == "__main__":
    servers = [
        Server("Server1", "US"),
        Server("Server2", "Europe"),
        Server("Server3", "Asia"),
        Server("Server4", "India")
    ]

    # Correct relative path to trained model
    router = SmartRouter(servers, "../Phase3/cpu_load_predictor_rf.joblib")

    # Simulate 5 client requests
    for i in range(5):
        print(f"\nEvaluating for Request {i+1}:")
        chosen = router.choose_best_server()
        result = chosen.handle_request()
        print(f"=> Request {i+1}: Routed to {chosen.name} ({chosen.region}) [latency: {chosen.latency}ms]")
        print("   " + result)
