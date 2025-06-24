# /utils/csv_loader.py
import csv
import os

def load_csv_prompts(csv_path, max_rows=None):
    """
    Loads prompts from a CSV file with structure: ID,Original Prompt,Category

    Args:
        csv_path (str): Path to the CSV file.
        max_rows (int): Maximum number of rows to load.

    Returns:
        list[dict]: List of dictionaries with keys: id, prompt, category.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    prompts = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if max_rows and i >= max_rows:
                break
            prompts.append({
                "id": row["ID"].strip(),
                "prompt": row["Original Prompt"].strip(),
                "category": row["Category"].strip().lower().replace(" ", "_")
            })

    return prompts
