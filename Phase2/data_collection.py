import csv
import random
import time
import math
from datetime import datetime, timedelta
from Phase1 import Server
# Reuse your Server class from previous phases (with get_metrics and handle_request)
class Server:
    def __init__(self, name, region):
        self.name = name
        self.region = region
        self.latency = random.randint(20, 100)     # ms
        self.cpu_load = random.uniform(0, 100)     # percentage
        self.packet_loss = random.uniform(0, 5)    # %
        self.jitter = random.uniform(0, 10)        # ms
        self.active_requests = 0

    def handle_request(self):
        self.active_requests += 1
        time.sleep(0.01)  # shortened sleep for simulation speed
        self.active_requests -= 1
        return f"Response from {self.name} in {self.region}"

    def get_metrics(self, current_time):
        # Base CPU load for each region
        base_cpu = {'US': 40, 'Europe': 30, 'Asia': 50, 'India': 40}
    
    # Simulate a daily peak time for each region (in hours)
        peak_hour = {'US': 15, 'Europe': 14, 'Asia': 11, 'India': 17}

    # Calculate a cyclical pattern based on the hour of the day
        hour = current_time.hour
        peak = peak_hour[self.region]
    
        # This creates a wave-like pattern that peaks at the specified hour
        cyclical_load = (math.sin((hour - peak) * (math.pi / 12)) + 1) / 2 * 50  # Ranges from 0 to 50
        
        # Add some random noise to make it more realistic
        noise = random.uniform(-5, 5)
        
        # Combine base load, cyclical pattern, and noise
        self.cpu_load = max(0, min(100, base_cpu[self.region] + cyclical_load + noise))
        
        # Keep other metrics random for now
        self.latency = random.randint(20, 100)
        self.packet_loss = random.uniform(0, 5)
        self.jitter = random.uniform(0, 10)
    
        return {
        "latency": self.latency,
        "cpu_load": self.cpu_load,
        "packet_loss": self.packet_loss,
        "jitter": self.jitter,
        "active_requests": self.active_requests
    }

    
    

# Initialize servers
servers = [
    Server("Server1", "US"),
    Server("Server2", "Europe"),
    Server("Server3", "Asia"),
    Server("Server4", "India")
]

# Simulation parameters
start_time = datetime(2025, 8, 1, 0, 0, 0)  # arbitrary start datetime
num_minutes = 7 * 24 * 60  # 1 week of data (in minutes)
time_step = timedelta(minutes=1)

# Prepare CSV file
csv_filename = "server_metrics_week.csv"
with open(csv_filename, mode='w', newline='') as csvfile:
    fieldnames = ["timestamp", "server_name", "region", "latency_ms", "cpu_load_percent",
                  "packet_loss_percent", "jitter_ms", "active_requests"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    current_time = start_time
    for _ in range(num_minutes):
        for server in servers:
            # Pass the current time to the get_metrics function
            metrics = server.get_metrics(current_time) 

            # Optional: simulate random incoming requests for more realistic active_requests dynamics
            incoming_requests = random.randint(0, 5)
            for _ in range(incoming_requests):
                server.handle_request()

            # Log metrics with timestamp
            writer.writerow({
                "timestamp": current_time.isoformat(),
                "server_name": server.name,
                "region": server.region,
                "latency_ms": metrics["latency"],
                "cpu_load_percent": metrics["cpu_load"],
                "packet_loss_percent": metrics["packet_loss"],
                "jitter_ms": metrics["jitter"],
                "active_requests": metrics["active_requests"]
            })

        current_time += time_step

print(f"Data logging complete! Metrics saved to {csv_filename}")
