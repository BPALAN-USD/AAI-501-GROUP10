import streamlit as st
import os


# --- LOG FILES VIEWER ---
# Make sure logs_directory matches your logs folder exactly
BASE_DIR = os.path.abspath(os.getcwd())
logs_directory = os.path.join(BASE_DIR, "logs")  # your logs folder path

if os.path.exists(logs_directory):

    if st.button("Clear Logs"):
        cleared_any = False
        for filename in os.listdir(logs_directory):
            file_path = os.path.join(logs_directory, filename)
            if os.path.isfile(file_path):
                # Open file in write mode to truncate it (clear contents)
                with open(file_path, "w") as f:
                    pass
                cleared_any = True
        if cleared_any:
            st.success("All log files have been cleared.")
        else:
            st.info("No log files to clear.")

    log_files = [f for f in os.listdir(logs_directory) if os.path.isfile(os.path.join(logs_directory, f))]

    if log_files:
        with st.expander("Show Log Files"):
            tabs = st.tabs(log_files)
            for i, log_file in enumerate(log_files):
                with tabs[i]:
                    log_path = os.path.join(logs_directory, log_file)
                    try:
                        with open(log_path, "r") as f:
                            content = f.read()
                        st.code(content, language="log")
                    except Exception as e:
                        st.error(f"Could not read log file {log_file}: {e}")
    else:
        st.info("No log files found.")
else:
    st.warning(f"Logs directory does not exist: {logs_directory}")