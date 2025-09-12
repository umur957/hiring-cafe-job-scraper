# Hiring.cafe Job Scraper

A Python-based web scraper for extracting job listings from hiring.cafe using their official API. The scraper can search for jobs based on various criteria and export the results to Excel format.

## Features

- **Comprehensive Job Search**: Search for jobs using any keyword or term
- **Full API Integration**: Uses hiring.cafe's official API endpoints
- **Pagination Support**: Automatically handles multiple pages of results
- **Excel Export**: Convert JSON results to Excel files with automatic chunking for large datasets
- **Data Processing**: Clean HTML content and handle special characters
- **Error Handling**: Robust error handling with detailed logging

## Files

- `job_scraper.py` - Main scraper script for extracting job data
- `excel_converter.py` - Utility to convert JSON results to Excel format
- `README.md` - This documentation file

## Prerequisites

Install the required Python packages:

```bash
pip install requests pandas beautifulsoup4 openpyxl
```

## Usage

### 1. Scraping Jobs

Run the main scraper script:

```bash
python job_scraper.py
```

You'll be prompted to enter a search term (e.g., "Data Scientist", "Software Engineer", "Remote", etc.).

The script will:
- Search for jobs matching your criteria
- Handle pagination automatically
- Save results to a JSON file named `{search_term}_jobs.json`

### 2. Converting to Excel

After scraping, convert the JSON data to Excel format:

```bash
python excel_converter.py
```

Enter the JSON filename when prompted. The script will:
- Convert JSON data to Excel format
- Split large datasets into multiple files (10,000 rows each)
- Create summary sheets with statistics
- Generate an overall summary file

## Example Usage

```python
from job_scraper import scrape_hiring_cafe_jobs, save_jobs_to_json

# Scrape jobs for a specific search term
jobs = scrape_hiring_cafe_jobs("Python Developer")

# Save to JSON
save_jobs_to_json(jobs, "python_developer_jobs.json")

print(f"Found {len(jobs)} jobs!")
```

## Data Structure

Each job record contains the following fields:

- `id` - Unique job identifier
- `board_token` - Job board token
- `source` - Job source/company
- `apply_url` - Direct application URL
- `title` - Job title (cleaned)
- `description_clean` - Job description (HTML removed)
- `description_raw` - Original job description
- `viewed_count` - Number of views
- `applied_count` - Number of applications
- `saved_count` - Number of saves
- `hidden_count` - Number of hides

## Configuration

The scraper uses the following default settings:

- **Location**: United States (can be modified in search_state)
- **Workplace Types**: Remote, Hybrid, Onsite
- **Commitment Types**: Full Time, Part Time, Contract, Internship, etc.
- **Seniority Levels**: No Experience Required, Entry Level, Mid Level
- **Date Range**: Last 61 days
- **Page Size**: 1000 jobs per request (maximum)

## Output Files

### JSON Output
- `{search_term}_jobs.json` - Raw job data

### Excel Output
- `{search_term}_part_1.xlsx`, `{search_term}_part_2.xlsx`, etc. - Job data (max 10,000 rows each)
- `{search_term}_overall_summary.xlsx` - Summary statistics and file breakdown

Each Excel file includes:
- **Jobs Data** sheet - Main job listings
- **Summary** sheet - Statistics for that chunk
- **Top Companies** sheet (summary file only)
- **File Breakdown** sheet (summary file only)

## Error Handling

The scraper includes comprehensive error handling for:
- Network timeouts and connection errors
- Invalid JSON responses
- Rate limiting (with automatic retry logic)
- Excel character encoding issues
- Large dataset processing

## Rate Limiting

The scraper is designed to be respectful of the hiring.cafe servers:
- Uses appropriate headers to mimic browser requests
- Implements reasonable delays between requests
- Handles server errors gracefully

## Troubleshooting

### Common Issues

1. **No jobs found**: Try different search terms or check if the site is accessible
2. **Excel encoding errors**: The converter automatically handles special characters
3. **Large datasets**: Files are automatically split into chunks for Excel compatibility
4. **Network errors**: Check your internet connection and try again

### Debug Mode

For debugging, check the console output which includes:
- API response status codes
- Number of jobs found per page
- Error messages and stack traces

## Legal Notice

This tool is for educational and research purposes. Please respect hiring.cafe's terms of service and use the scraper responsibly. Don't overwhelm their servers with excessive requests.

## License

This project is open source and available under the MIT License.