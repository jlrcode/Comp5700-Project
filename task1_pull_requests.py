#!/usr/bin/env python3
"""
Task-1: Extract data from all_pull_request table and create CSV
Creates CSV with: TITLE, ID, AGENTNAME, BODYSTRING, REPOID, REPOURL
"""

from datasets import load_dataset
import pandas as pd
import os

def process_task1():
    """Process Task-1: Extract pull request data"""
    print("Loading all_pull_request dataset...")
    
    # Load the all_pull_request configuration
    dataset = load_dataset("hao-li/AIDev", "all_pull_request")
    data = dataset["train"]
    
    print(f"Loaded {len(data)} pull requests")
    print(f"Columns available: {data.column_names}")
    
    # Convert to pandas DataFrame for easier processing
    df = data.to_pandas()
    
    # Create the required CSV structure
    task1_df = pd.DataFrame({
        'TITLE': df['title'],
        'ID': df['id'],
        'AGENTNAME': df['agent'],
        'BODYSTRING': df['body'],
        'REPOID': df['repo_id'],
        'REPOURL': df['repo_url']
    })
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Save to CSV
    output_file = 'output/task1_pull_requests.csv'
    task1_df.to_csv(output_file, index=False)
    
    print(f"Task-1 completed! CSV saved to: {output_file}")
    print(f"Total records: {len(task1_df)}")
    print(f"Sample data:")
    print(task1_df.head())

if __name__ == "__main__":
    process_task1()