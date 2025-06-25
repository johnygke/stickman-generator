
import pandas as pd
def load_csv_prompts(uploaded_file):
    import pandas as pd
    df = pd.read_csv(uploaded_file)
    return df.to_dict(orient="records")
