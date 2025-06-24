
import pandas as pd

def load_prompts_from_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    prompts = df.to_dict(orient='records')
    return prompts
