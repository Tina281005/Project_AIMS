import random
import time

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
        time.sleep(0.1)
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
    # Assign weights to each metric (must add up to 1.0)
    WEIGHTS = {
        "latency": 0.4,
        "cpu_load": 0.2,
        "packet_loss": 0.15,
        "jitter": 0.15,
        "active_requests": 0.1,
    }
    # Normalization constants (upper bounds for each metric)
    NORMALIZE = {
        "latency": 100,         # ms (range is 20-100)
        "cpu_load": 100,        # percentage
        "packet_loss": 5,       # percent
        "jitter": 10,           # ms
        "active_requests": 10,  # Assume max 10 for demo
    }

    def __init__(self, servers):
        self.servers = servers

    def calculate_score(self, metrics):
        # Normalize and weight each metric, then sum
        score = 0.0
        for metric in self.WEIGHTS:
            value = metrics[metric]
            max_value = self.NORMALIZE[metric]
            normalized = min(value / max_value, 1.0)  # Clamp to 1.0
            score += normalized * self.WEIGHTS[metric]
        return score

    def choose_best_server(self):
        best_server = None
        best_score = float("inf")
        for s in self.servers:
            metrics = s.get_metrics()
            score = self.calculate_score(metrics)
            if score < best_score:
                best_score = score
                best_server = s
            # For demonstration, print each server's score:
            print(f"  {s.name} ({s.region}) - Score: {score:.3f} [latency: {metrics['latency']}ms, cpu: {metrics['cpu_load']:.1f}%, loss: {metrics['packet_loss']:.2f}%, jitter: {metrics['jitter']:.2f}ms, active: {metrics['active_requests']}]")
        return best_server

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

    router = SmartRouter(servers)

    # Simulate 5 client requests
    for i in range(5):
        print(f"\nEvaluating for Request {i+1}:")
        chosen = router.choose_best_server()
        result = chosen.handle_request()
        print(f"=> Request {i+1}: Routed to {chosen.name} ({chosen.region}) [latency: {chosen.latency}ms]")
        print("   " + result)
