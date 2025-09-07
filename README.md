🧠 AI-Enhanced CDN Smart Router :-
This project is a simulation of a modern Content Delivery Network (CDN) that uses a predictive, AI-enhanced smart router to perform intelligent server selection. Unlike traditional CDNs that route based on latency alone, this router considers multiple real-time metrics and uses a machine learning model to predict future server load, moving from a reactive to a predictive routing strategy.

✨ Features
Multi-Metric Routing: The smart router calculates a weighted health score for each server based on latency, CPU load, packet loss, jitter, and active requests.

AI-Powered Predictions: A RandomForestRegressor model, trained on a week's worth of simulated server data, predicts future CPU load based on time-of-day and day-of-week patterns.

Predictive over Reactive: By factoring in the AI prediction, the router can proactively avoid servers that are likely to become overloaded, even if their current metrics look good.

Live Monitoring Dashboard: An interactive web dashboard built with Streamlit provides a real-time view of server health, AI predictions, and the router's decisions.

🚀 How It Works
The project is composed of three main parts:

Data Collection (data_collection.py): A script that simulates four servers across different global regions (US, Europe, Asia, India). It generates a week of realistic, patterned metric data, where each server has unique daily peak hours. This data is saved to server_metrics_week.csv.

Model Training (trainmodel.py): This script reads the collected data, engineers time-based features (hour, day of the week), and trains a Random Forest model to predict the next minute's CPU load. The trained model is saved as cpu_load_predictor_rf.joblib.

Live Simulation & Dashboard (dashboard.py & Server.py):

The Server.py module contains the core logic for the Server and SmartRouter classes.

The dashboard.py script launches a Streamlit web application.

In real-time, the dashboard simulates client requests. For each request, the SmartRouter fetches current metrics from all servers, queries the AI model for a future CPU load prediction, calculates a final health score, and routes the request to the server with the best (lowest) score.

The dashboard visualizes this entire process, updating every few seconds.

🛠️ Technology Stack
Backend: Python

Machine Learning: Scikit-learn, Pandas

Dashboard: Streamlit

Core Libraries: Joblib, NumPy

📦 Installation & Setup
Clone the repository:

Bash

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Install the required libraries:

Bash

pip install scikit-learn pandas joblib streamlit
🏃‍♂️ How to Run the Project
You can run the project in three stages:

(Optional) Generate New Data: If you want to generate a new dataset, run the data collection script.

Bash

python data_collection.py
(Optional) Retrain the AI Model: If you generated new data or want to retrain the model, run the training script.

Bash

python trainmodel.py
Run the Live Dashboard: This is the main entry point to see the project in action.

Bash

streamlit run dashboard.py
Your web browser will automatically open with the live dashboard.
