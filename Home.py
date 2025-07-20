import streamlit as st
from utils.getDataset import *
import os
from utils.logger_setup import *

st.set_page_config(page_title="Autonomous Car Team 10", layout="wide")
st.title("Autonomous Car Team 10")

logger = get_logger("main_application.log")

logger.info("Main Application Executed.")



