#!/usr/bin/env python3
"""
Task-4: Extract data from pr_commit_details table and create CSV
Creates CSV with: PRID, PRSHA, PRCOMMITMESSAGE, PRFILE, PRSTATUS, PRADDS, PRDELSS, PRCHANGECOUNT, PRDIFF
Note: PRDIFF field needs special character cleaning to avoid string encoding errors
"""

from datasets import load_dataset
import pandas as pd
import os
import re

def clean_patch_data(patch_text):
    """Clean patch data to remove special characters that cause encoding errors"""
    if patch_text is None or pd.isna(patch_text):
        return ""
    
    # Convert to string if not already
    patch_str = str(patch_text)
    
    # Remove control characters (except newlines, tabs, and carriage returns)
    # Keep printable ASCII and common whitespace characters
    cleaned = re.sub(r'[^\x20-\x7E\n\r\t]', '', patch_str)
    
    # Remove any remaining problematic characters that might cause CSV issues
    cleaned = cleaned.replace('\x00', '')  # Remove null bytes
    cleaned = re.sub(r'[\x01-\x08\x0B\x0C\x0E-\x1F\x7F-\xFF]', '', cleaned)
    
    # Replace multiple consecutive whitespaces with single space (except newlines)
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)
    
    return cleaned.strip()

def process_task4():
    """Process Task-4: Extract PR commit details data"""
    print("Loading pr_commit_details dataset...")
    
    # Load the pr_commit_details configuration
    dataset = load_dataset("hao-li/AIDev", "pr_commit_details")
    data = dataset["train"]
    
    print(f"Loaded {len(data)} PR commit details records")
    print(f"Columns available: {data.column_names}")
    
    # Convert to pandas DataFrame for easier processing
    df = data.to_pandas()
    
    print("Cleaning patch data...")
    # Apply the cleaning function to the patch column
    df['cleaned_patch'] = df['patch'].apply(clean_patch_data)
    
    # Create the required CSV structure
    task4_df = pd.DataFrame({
        'PRID': df['pr_id'],
        'PRSHA': df['sha'],
        'PRCOMMITMESSAGE': df['message'],
        'PRFILE': df['filename'],
        'PRSTATUS': df['status'],
        'PRADDS': df['additions'],
        'PRDELSS': df['deletions'],
        'PRCHANGECOUNT': df['changes'],
        'PRDIFF': df['cleaned_patch']
    })
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Save to CSV with proper encoding
    output_file = 'output/task4_pr_commit_details.csv'
    task4_df.to_csv(output_file, index=False, encoding='utf-8', errors='replace')
    
    print(f"Task-4 completed! CSV saved to: {output_file}")
    print(f"Total records: {len(task4_df)}")
    print(f"Sample data:")
    print(task4_df[['PRID', 'PRSHA', 'PRFILE', 'PRSTATUS', 'PRADDS', 'PRDELSS']].head())
    print(f"Sample cleaned diff (first 200 chars): {task4_df['PRDIFF'].iloc[0][:200] if len(task4_df) > 0 else 'No data'}")

if __name__ == "__main__":
    process_task4()