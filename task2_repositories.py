#!/usr/bin/env python3
"""
Task-2: Extract data from all_repository table and create CSV
Creates CSV with: REPOID, LANG, STARS, REPOURL
"""

from datasets import load_dataset
import pandas as pd
import os

def process_task2():
    """Process Task-2: Extract repository data"""
    print("Loading all_repository dataset...")
    
    # Load the all_repository configuration
    dataset = load_dataset("hao-li/AIDev", "all_repository")
    data = dataset["train"]
    
    print(f"Loaded {len(data)} repositories")
    print(f"Columns available: {data.column_names}")
    
    # Convert to pandas DataFrame for easier processing
    df = data.to_pandas()
    
    # Create the required CSV structure
    task2_df = pd.DataFrame({
        'REPOID': df['id'],
        'LANG': df['language'],
        'STARS': df['stars'],
        'REPOURL': df['url']
    })
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Save to CSV
    output_file = 'output/task2_repositories.csv'
    task2_df.to_csv(output_file, index=False)
    
    print(f"Task-2 completed! CSV saved to: {output_file}")
    print(f"Total records: {len(task2_df)}")
    print(f"Sample data:")
    print(task2_df.head())

if __name__ == "__main__":
    process_task2()