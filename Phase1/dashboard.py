import streamlit as st
import pandas as pd
import time
from Server import Server, SmartRouter # Import your existing classes

# --- Page Configuration ---
st.set_page_config(
    page_title="Live CDN Smart Router Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Initialize Session State ---
# This is like a memory for your app
if 'log_messages' not in st.session_state:
    st.session_state['log_messages'] = []

# --- Main Dashboard Setup ---
st.title("📡 Live CDN Smart Router Dashboard")
st.text(f"Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")

# --- Initialize Servers and Router ---
# Make sure the paths are correct for your project structure
servers = [
    Server("Server1", "US"),
    Server("Server2", "Europe"),
    Server("Server3", "Asia"),
    Server("Server4", "India")
]
# --- This is the corrected path ---
router = SmartRouter(servers, "../Phase3/cpu_load_predictor_rf.joblib")

# --- Dashboard Layout ---
# Create placeholders to update content without redrawing the whole page
placeholder = st.empty()

# --- Main Loop to Simulate Live Data ---
for i in range(1000): # The loop will run for 1000 iterations
    with placeholder.container():
        # --- Get Server Metrics in a DataFrame ---
        all_metrics = []
        for s in servers:
            metrics = s.get_metrics()
            metrics['server_name'] = s.name
            metrics['region'] = s.region
            all_metrics.append(metrics)
        
        df = pd.DataFrame(all_metrics).set_index('server_name')

        # --- Top-Level Metrics ---
        st.header("🏆 Live Performance Leaders")
        
        # --- Get the router's decision first ---
        chosen_server, scores_df = router.choose_best_server_with_scores()

        # --- Create 4 columns for the KPIs ---
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        # --- The New "Overall Best" Card ---
        with kpi1:
            st.markdown(f"<h3 style='text-align: center; color: green;'>Overall Best Server</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; font-size: 24px;'><strong>{chosen_server.name}</strong> ({chosen_server.region})</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>Score: {scores_df.loc[chosen_server.name, 'score']:.3f}</p>", unsafe_allow_html=True)
        
        # --- The other leader cards ---
        lowest_latency_server = scores_df['latency'].idxmin()
        kpi2.metric(label="Lowest Latency", value=f"{lowest_latency_server}", delta=f"{scores_df.loc[lowest_latency_server, 'latency']} ms")

        lowest_cpu_server = scores_df['cpu_load'].idxmin()
        kpi3.metric(label="Lowest CPU Load", value=f"{lowest_cpu_server}", delta=f"{scores_df.loc[lowest_cpu_server, 'cpu_load']:.1f} %")
        
        lowest_loss_server = scores_df['packet_loss'].idxmin()
        kpi4.metric(label="Lowest Packet Loss", value=f"{lowest_loss_server}", delta=f"{scores_df.loc[lowest_loss_server, 'packet_loss']:.2f} %")
        
        st.markdown("<hr/>", unsafe_allow_html=True)

        # --- Main Sections: Server Details and Decision Log ---
        col1, col2 = st.columns([3, 2]) # Make the first column wider

        with col1:
            st.header("📊 Server Health Details")
            
            # --- Router makes its decision ---
            #chosen_server, scores_df = router.choose_best_server_with_scores()

            # --- Color-coding the DataFrame for visual appeal ---
            def style_df(df):
                return df.style.background_gradient(cmap='RdYlGn_r', subset=['score', 'cpu_load', 'predicted_cpu_load', 'latency']) \
                               .format("{:.2f}", subset=['cpu_load', 'packet_loss', 'jitter', 'score', 'predicted_cpu_load']) \
                               .format("{:.0f}", subset=['latency']) \
                               .set_properties(**{'text-align': 'center'})

            st.dataframe(style_df(scores_df), width="stretch")


        with col2:
            st.header("📜 Live Decision Log")
            
            # Add new log message to the top of the list
            log_entry = f"**{time.strftime('%H:%M:%S')}**: Request routed to **{chosen_server.name}** ({chosen_server.region}) with score **{scores_df.loc[chosen_server.name, 'score']:.3f}**."
            st.session_state.log_messages.insert(0, log_entry)

            # Display the log messages
            for msg in st.session_state.log_messages[:10]: # Show latest 10 logs
                st.info(msg)

    # --- Refresh Rate ---
    time.sleep(2) # Refresh every 2 seconds