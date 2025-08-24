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
        # simulate processing
        time.sleep(0.1)
        self.active_requests -= 1
        return f"Response from {self.name} in {self.region}"
    
    def get_metrics(self):
        # we could refresh metrics randomly to simulate changing conditions
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
    def __init__(self, servers):
        self.servers = servers

    def choose_server_latency_only(self):
        # pick server with the lowest latency
        best_server = min(self.servers, key=lambda s: s.get_metrics()['latency'])
        return best_server


# ----------------------
# Simulation Example
# ----------------------
if __name__ == "__main__":
    # create a few servers
    servers = [
        Server("Server1", "US"),
        Server("Server2", "Europe"),
        Server("Server3", "Asia"),
        Server("Server4", "India")
    ]

    router = SmartRouter(servers)

    # simulate 5 client requests
    for i in range(5):
        chosen = router.choose_server_latency_only()
        result = chosen.handle_request()
        print(f"Request {i+1}: Routed to {chosen.name} ({chosen.region}) with latency {chosen.latency}ms")
        print("   " + result)
