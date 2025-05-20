import pandas as pd
from typing import Dict, Union
import os

def save_and_parse_uploaded_files(uploaded_files) -> Dict[str, pd.DataFrame]:
    dataframes = {}
    os.makedirs("data", exist_ok=True)
    for uploaded_file in uploaded_files:
        file_path = os.path.join("data", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path, engine="openpyxl")
        dataframes[uploaded_file.name] = df
    return dataframes

