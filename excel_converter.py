import json
import pandas as pd
from bs4 import BeautifulSoup
import re

def clean_html_text(html_text):
    """
    Clean HTML tags from text and return plain text
    
    Args:
        html_text (str): HTML content to clean
        
    Returns:
        str: Clean text without HTML tags and illegal characters
    """
    if not html_text:
        return ""
    
    # Only process if it looks like HTML content, not filename
    if len(html_text) > 100 or '<' in html_text:
        soup = BeautifulSoup(html_text, 'html.parser')
        text = soup.get_text(strip=True)
    else:
        text = str(html_text)
    
    # Remove illegal characters for Excel
    illegal_chars = ['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', 
                    '\x08', '\x0b', '\x0c', '\x0e', '\x0f', '\x10', '\x11', '\x12', 
                    '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\x1a', 
                    '\x1b', '\x1c', '\x1d', '\x1e', '\x1f']
    for char in illegal_chars:
        text = text.replace(char, '')
    
    return text

def flatten_job_data(job):
    """
    Flatten nested job data structure for Excel export
    
    Args:
        job (dict): Job data dictionary
        
    Returns:
        dict: Flattened job data
    """
    flattened = {
        'id': job.get('id', ''),
        'board_token': job.get('board_token', ''),
        'source': job.get('source', ''),
        'apply_url': job.get('apply_url', ''),
        'source_and_board_token': job.get('source_and_board_token', ''),
    }
    
    # Extract job information
    job_info = job.get('job_information', {})
    flattened['title'] = clean_html_text(str(job_info.get('title', '')))
    flattened['description_clean'] = clean_html_text(job_info.get('description', ''))
    flattened['description_raw'] = clean_html_text(str(job_info.get('description', '')))
    
    # Count user interactions
    flattened['viewed_count'] = len(job_info.get('viewedByUsers', []))
    flattened['applied_count'] = len(job_info.get('appliedFromUsers', []))
    flattened['saved_count'] = len(job_info.get('savedFromUsers', []))
    flattened['hidden_count'] = len(job_info.get('hiddenFromUsers', []))
    
    return flattened

def convert_json_to_excel(json_file, output_prefix="jobs", chunk_size=10000):
    """
    Convert JSON job data to Excel files with chunking for large datasets
    
    Args:
        json_file (str): Path to input JSON file
        output_prefix (str): Prefix for output files
        chunk_size (int): Maximum rows per Excel file (default: 10000)
    
    Returns:
        list: List of created file names
    """
    print(f"Converting {json_file} to Excel format...")
    
    try:
        # Load JSON data
        with open(json_file, 'r', encoding='utf-8') as f:
            jobs_data = json.load(f)
        
        print(f"Loaded {len(jobs_data)} jobs from JSON")
        
        if not jobs_data:
            print("No job data found in JSON file")
            return []
        
        # Flatten data for Excel
        flattened_jobs = []
        for job in jobs_data:
            try:
                flattened = flatten_job_data(job)
                flattened_jobs.append(flattened)
            except Exception as e:
                print(f"Error processing job {job.get('id', 'unknown')}: {e}")
                continue
        
        if not flattened_jobs:
            print("No jobs could be processed")
            return []
        
        # Create DataFrame
        df = pd.DataFrame(flattened_jobs)
        
        # Calculate number of chunks needed
        total_chunks = (len(df) + chunk_size - 1) // chunk_size
        created_files = []
        
        print(f"Splitting {len(df)} jobs into {total_chunks} Excel file(s) ({chunk_size} rows each max)...")
        
        # Create chunked Excel files
        for i in range(0, len(df), chunk_size):
            chunk = df[i:i+chunk_size]
            part_number = i//chunk_size + 1
            filename = f'{output_prefix}_part_{part_number}.xlsx'
            
            print(f"Creating {filename} with {len(chunk)} jobs...")
            
            # Create Excel file for this chunk
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Main data sheet
                chunk.to_excel(writer, sheet_name='Jobs Data', index=False)
                
                # Add a summary sheet for this chunk
                chunk_summary = {
                    'Metric': [
                        f'Jobs in Part {part_number}',
                        'Unique Sources',
                        'Total Viewed',
                        'Total Applied',
                        'Total Saved',
                        'Total Hidden'
                    ],
                    'Value': [
                        len(chunk),
                        chunk['source'].nunique(),
                        chunk['viewed_count'].sum(),
                        chunk['applied_count'].sum(),
                        chunk['saved_count'].sum(),
                        chunk['hidden_count'].sum()
                    ]
                }
                chunk_summary_df = pd.DataFrame(chunk_summary)
                chunk_summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            print(f"Created {filename} successfully!")
            created_files.append(filename)
        
        # Create overall summary file
        summary_filename = f'{output_prefix}_overall_summary.xlsx'
        with pd.ExcelWriter(summary_filename, engine='openpyxl') as writer:
            # Overall summary
            summary_data = {
                'Metric': [
                    'Total Jobs',
                    'Total Excel Files',
                    'Jobs per File (Max)',
                    'Unique Sources',
                    'Total Viewed',
                    'Total Applied', 
                    'Total Saved',
                    'Total Hidden'
                ],
                'Value': [
                    len(df),
                    total_chunks,
                    chunk_size,
                    df['source'].nunique(),
                    df['viewed_count'].sum(),
                    df['applied_count'].sum(),
                    df['saved_count'].sum(),
                    df['hidden_count'].sum()
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Overall Summary', index=False)
            
            # Top companies (top 50)
            top_companies = df['source_and_board_token'].value_counts().head(50)
            top_companies_df = pd.DataFrame({
                'Company_Board': top_companies.index,
                'Job_Count': top_companies.values
            })
            top_companies_df.to_excel(writer, sheet_name='Top Companies', index=False)
            
            # File breakdown
            file_breakdown = []
            for i in range(total_chunks):
                start_idx = i * chunk_size
                end_idx = min((i + 1) * chunk_size, len(df))
                file_breakdown.append({
                    'File_Name': f'{output_prefix}_part_{i+1}.xlsx',
                    'Rows': end_idx - start_idx,
                    'Start_Index': start_idx + 1,
                    'End_Index': end_idx
                })
            
            breakdown_df = pd.DataFrame(file_breakdown)
            breakdown_df.to_excel(writer, sheet_name='File Breakdown', index=False)
        
        created_files.append(summary_filename)
        
        print(f"\nSuccessfully created {total_chunks} Excel file(s)!")
        print(f"Overall summary: {summary_filename}")
        print(f"Each file contains max {chunk_size:,} rows")
        print(f"Total data: {len(df):,} jobs across {len(df.columns)} columns")
        print(f"\nFiles created:")
        for file in created_files:
            print(f"  - {file}")
        
        return created_files
        
    except FileNotFoundError:
        print(f"Error: JSON file '{json_file}' not found")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_file}'")
        return []
    except Exception as e:
        print(f"Error converting to Excel: {e}")
        return []

if __name__ == "__main__":
    # Example usage
    json_filename = input("Enter JSON filename to convert: ")
    
    if not json_filename.endswith('.json'):
        json_filename += '.json'
    
    # Extract prefix from filename for output files
    output_prefix = json_filename.replace('.json', '').replace('_jobs', '')
    
    # Convert to Excel
    created_files = convert_json_to_excel(json_filename, output_prefix)
    
    if created_files:
        print(f"\nConversion completed successfully!")
        print(f"Created {len(created_files)} file(s)")
    else:
        print("\nConversion failed!")