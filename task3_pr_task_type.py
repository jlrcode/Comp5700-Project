#!/usr/bin/env python3
"""
Task-3: Extract data from pr_task_type table and create CSV
Creates CSV with: PRID, PRTITLE, PRREASON, PRTYPE, CONFIDENCE
"""

from datasets import load_dataset
import pandas as pd
import os

def process_task3():
    """Process Task-3: Extract PR task type data"""
    print("Loading pr_task_type dataset...")
    
    # Load the pr_task_type configuration
    dataset = load_dataset("hao-li/AIDev", "pr_task_type")
    data = dataset["train"]
    
    print(f"Loaded {len(data)} PR task type records")
    print(f"Columns available: {data.column_names}")
    
    # Convert to pandas DataFrame for easier processing
    df = data.to_pandas()
    
    # Create the required CSV structure
    task3_df = pd.DataFrame({
        'PRID': df['id'],
        'PRTITLE': df['title'],
        'PRREASON': df['reason'],
        'PRTYPE': df['type'],
        'CONFIDENCE': df['confidence']
    })
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Save to CSV
    output_file = 'output/task3_pr_task_type.csv'
    task3_df.to_csv(output_file, index=False)
    
    print(f"Task-3 completed! CSV saved to: {output_file}")
    print(f"Total records: {len(task3_df)}")
    print(f"Sample data:")
    print(task3_df.head())

if __name__ == "__main__":
    process_task3()