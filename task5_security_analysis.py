#!/usr/bin/env python3
"""
Task-5: Create combined CSV with security analysis
Combines data from previous tasks and adds security keyword analysis
Creates CSV with: ID, AGENT, TYPE, CONFIDENCE, SECURITY
"""

import pandas as pd
import os
import re

def load_previous_tasks():
    """Load CSVs from previous tasks"""
    task1_df = pd.read_csv('output/task1_pull_requests.csv')
    task3_df = pd.read_csv('output/task3_pr_task_type.csv')
    
    return task1_df, task3_df

def check_security_keywords(text):
    """
    Check if security-related keywords appear in text
    Returns 1 if security keywords found, 0 otherwise
    """
    if pd.isna(text) or text is None:
        return 0
    
    # Security keywords from the README references section
    security_keywords = [
        'race', 'racy', 'buffer', 'overflow', 'stack', 'integer', 'signedness', 
        'underflow', 'improper', 'unauthenticated', 'gain access', 'permission', 
        'cross site', 'css', 'xss', 'denial service', 'dos', 'crash', 'deadlock', 
        'injection', 'request forgery', 'csrf', 'xsrf', 'forged', 'security', 
        'vulnerability', 'vulnerable', 'exploit', 'attack', 'bypass', 'backdoor', 
        'threat', 'expose', 'breach', 'violate', 'fatal', 'blacklist', 'overrun', 
        'insecure'
    ]
    
    # Convert text to lowercase for case-insensitive matching
    text_lower = str(text).lower()
    
    # Check for each keyword
    for keyword in security_keywords:
        if keyword in text_lower:
            return 1
    
    return 0

def process_task5():
    """Process Task-5: Create combined CSV with security analysis"""
    print("Loading data from previous tasks...")
    
    # Load data from previous tasks
    task1_df, task3_df = load_previous_tasks()
    
    print(f"Loaded {len(task1_df)} pull requests")
    print(f"Loaded {len(task3_df)} task type records")
    
    # Merge the dataframes on PR ID
    # task1_df has 'ID' column, task3_df has 'PRID' column
    merged_df = pd.merge(task1_df, task3_df, left_on='ID', right_on='PRID', how='inner')
    
    print(f"Merged dataset has {len(merged_df)} records")
    
    # Analyze security keywords in title and body
    print("Analyzing security keywords...")
    merged_df['title_security'] = merged_df['TITLE'].apply(check_security_keywords)
    merged_df['body_security'] = merged_df['BODYSTRING'].apply(check_security_keywords)
    
    # SECURITY flag is 1 if either title or body contains security keywords
    merged_df['SECURITY'] = ((merged_df['title_security'] == 1) | 
                            (merged_df['body_security'] == 1)).astype(int)
    
    # Create the final CSV structure for Task-5
    task5_df = pd.DataFrame({
        'ID': merged_df['ID'],
        'AGENT': merged_df['AGENTNAME'],
        'TYPE': merged_df['PRTYPE'],
        'CONFIDENCE': merged_df['CONFIDENCE'],
        'SECURITY': merged_df['SECURITY']
    })
    
    # Save to CSV
    output_file = 'output/task5_security_analysis.csv'
    task5_df.to_csv(output_file, index=False)
    
    print(f"Task-5 completed! CSV saved to: {output_file}")
    print(f"Total records: {len(task5_df)}")
    
    # Print some statistics
    security_count = task5_df['SECURITY'].sum()
    print(f"Records with security keywords: {security_count} ({security_count/len(task5_df)*100:.1f}%)")
    
    print(f"Sample data:")
    print(task5_df.head())
    
    # Show some examples of security-flagged records
    security_records = merged_df[merged_df['SECURITY'] == 1][['TITLE', 'BODYSTRING']].head(3)
    if len(security_records) > 0:
        print(f"\nSample security-flagged records:")
        for i, (_, row) in enumerate(security_records.iterrows()):
            print(f"  Example {i+1} Title: {row['TITLE'][:100]}...")

if __name__ == "__main__":
    process_task5()