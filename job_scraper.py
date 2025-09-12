import requests
import json

def scrape_hiring_cafe_jobs(search_query):
    """
    Scrape job listings from hiring.cafe API based on search query
    
    Args:
        search_query (str): The search term for job listings
    
    Returns:
        list: List of job dictionaries or empty list if failed
    """
    
    # API endpoints
    base_url = "https://hiring.cafe"
    count_endpoint = f"{base_url}/api/search-jobs/get-total-count"
    jobs_endpoint = f"{base_url}/api/search-jobs"
    
    # Headers to mimic browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Referer': 'https://hiring.cafe/',
        'Origin': 'https://hiring.cafe',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    
    # Search state configuration - comprehensive filter settings
    search_state = {
        "locations": [{
            "formatted_address": "United States",
            "types": ["country"],
            "geometry": {
                "location": {
                    "lat": "39.8283",
                    "lon": "-98.5795"
                }
            },
            "id": "user_country",
            "address_components": [{
                "long_name": "United States",
                "short_name": "US",
                "types": ["country"]
            }],
            "options": {
                "flexible_regions": ["anywhere_in_continent", "anywhere_in_world"]
            }
        }],
        "workplaceTypes": ["Remote", "Hybrid", "Onsite"],
        "defaultToUserLocation": False,
        "userLocation": None,
        "physicalEnvironments": ["Office", "Outdoor", "Vehicle", "Industrial", "Customer-Facing"],
        "physicalLaborIntensity": ["Low", "Medium", "High"],
        "physicalPositions": ["Sitting", "Standing"],
        "oralCommunicationLevels": ["Low", "Medium", "High"],
        "computerUsageLevels": ["Low", "Medium", "High"],
        "cognitiveDemandLevels": ["Low", "Medium", "High"],
        "currency": {"label": "Any", "value": None},
        "frequency": {"label": "Any", "value": None},
        "minCompensationLowEnd": None,
        "minCompensationHighEnd": None,
        "maxCompensationLowEnd": None,
        "maxCompensationHighEnd": None,
        "restrictJobsToTransparentSalaries": False,
        "calcFrequency": "Yearly",
        "commitmentTypes": ["Full Time", "Part Time", "Contract", "Internship", "Temporary", "Seasonal", "Volunteer"],
        "jobTitleQuery": "",
        "jobDescriptionQuery": "",
        "associatesDegreeFieldsOfStudy": [],
        "excludedAssociatesDegreeFieldsOfStudy": [],
        "bachelorsDegreeFieldsOfStudy": [],
        "excludedBachelorsDegreeFieldsOfStudy": [],
        "mastersDegreeFieldsOfStudy": [],
        "excludedMastersDegreeFieldsOfStudy": [],
        "doctorateDegreeFieldsOfStudy": [],
        "excludedDoctorateDegreeFieldsOfStudy": [],
        "associatesDegreeRequirements": [],
        "bachelorsDegreeRequirements": [],
        "mastersDegreeRequirements": [],
        "doctorateDegreeRequirements": [],
        "licensesAndCertifications": [],
        "excludedLicensesAndCertifications": [],
        "excludeAllLicensesAndCertifications": False,
        "seniorityLevel": ["No Prior Experience Required", "Entry Level", "Mid Level"],
        "roleTypes": ["Individual Contributor", "People Manager"],
        "roleYoeRange": [0, 20],
        "excludeIfRoleYoeIsNotSpecified": False,
        "managementYoeRange": [0, 20],
        "excludeIfManagementYoeIsNotSpecified": False,
        "securityClearances": ["None", "Confidential", "Secret", "Top Secret", "Top Secret/SCI", "Public Trust", "Interim Clearances", "Other"],
        "languageRequirements": [],
        "excludedLanguageRequirements": [],
        "languageRequirementsOperator": "OR",
        "excludeJobsWithAdditionalLanguageRequirements": False,
        "airTravelRequirement": ["None", "Minimal", "Moderate", "Extensive"],
        "landTravelRequirement": ["None", "Minimal", "Moderate", "Extensive"],
        "morningShiftWork": [],
        "eveningShiftWork": [],
        "overnightShiftWork": [],
        "weekendAvailabilityRequired": "Doesn't Matter",
        "holidayAvailabilityRequired": "Doesn't Matter",
        "overtimeRequired": "Doesn't Matter",
        "onCallRequirements": ["None", "Occasional (once a month or less)", "Regular (once a week or more)"],
        "benefitsAndPerks": [],
        "applicationFormEase": [],
        "companyNames": [],
        "excludedCompanyNames": [],
        "usaGovPref": None,
        "industries": [],
        "excludedIndustries": [],
        "companyKeywords": [],
        "companyKeywordsBooleanOperator": "OR",
        "excludedCompanyKeywords": [],
        "hideJobTypes": [],
        "encouragedToApply": [],
        "searchQuery": search_query,  # Dynamic search query
        "dateFetchedPastNDays": 61,
        "hiddenCompanies": [],
        "user": None,
        "searchModeSelectedCompany": None,
        "departments": [],
        "restrictedSearchAttributes": [],
        "sortBy": "default",
        "technologyKeywordsQuery": "",
        "requirementsKeywordsQuery": "",
        "companyPublicOrPrivate": "all",
        "latestInvestmentYearRange": [None, None],
        "latestInvestmentSeries": [],
        "latestInvestmentAmount": None,
        "latestInvestmentCurrency": [],
        "investors": [],
        "excludedInvestors": [],
        "isNonProfit": "all",
        "companySizeRanges": [],
        "minYearFounded": None,
        "maxYearFounded": None,
        "excludedLatestInvestmentSeries": []
    }
    
    # Request payloads
    count_payload = {
        "searchState": search_state
    }
    
    jobs_payload = {
        "size": 1000,  # Maximum page size
        "page": 0,
        "searchState": search_state
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        # Get total count first
        print(f"Getting total count for '{search_query}'...")
        count_response = session.post(count_endpoint, json=count_payload, timeout=30)
        print(f"Count API Status: {count_response.status_code}")
        
        total_jobs = 0
        if count_response.status_code == 200:
            try:
                count_data = count_response.json()
                print(f"Count response: {count_data}")
                if isinstance(count_data, dict) and 'total' in count_data:
                    total_jobs = count_data['total']
                    print(f"Total jobs available: {total_jobs}")
            except:
                print("Count response not JSON:", count_response.text[:200])
        
        # Scrape jobs with pagination
        all_jobs = []
        page = 0
        
        while True:
            print(f"\nGetting page {page} with size 1000...")
            jobs_payload["page"] = page
            
            jobs_response = session.post(jobs_endpoint, json=jobs_payload, timeout=30)
            print(f"Jobs API Status: {jobs_response.status_code}")
            
            if jobs_response.status_code == 200:
                try:
                    jobs_data = jobs_response.json()
                    print(f"Jobs response type: {type(jobs_data)}")
                    
                    current_batch = []
                    
                    if isinstance(jobs_data, dict):
                        print(f"Jobs response keys: {list(jobs_data.keys())}")
                        
                        # Look for job data in various possible keys
                        possible_keys = ['results', 'jobs', 'data', 'items', 'content']
                        for key in possible_keys:
                            if key in jobs_data and isinstance(jobs_data[key], list):
                                current_batch = jobs_data[key]
                                print(f"Found jobs in '{key}': {len(current_batch)} items")
                                break
                        
                        if not current_batch and 'hits' in jobs_data:
                            # Elasticsearch-style response
                            hits = jobs_data['hits']
                            if isinstance(hits, dict) and 'hits' in hits:
                                current_batch = [hit.get('_source', hit) for hit in hits['hits']]
                                print(f"Found jobs in Elasticsearch format: {len(current_batch)} items")
                        
                    elif isinstance(jobs_data, list):
                        current_batch = jobs_data
                        print(f"Got direct list with {len(current_batch)} jobs")
                    
                    if not current_batch:
                        print("No jobs found in this batch")
                        break
                    
                    # Add to our collection
                    all_jobs.extend(current_batch)
                    print(f"Total jobs collected so far: {len(all_jobs)}")
                    
                    # Check if we have more pages
                    if len(current_batch) < 1000 or (total_jobs > 0 and len(all_jobs) >= total_jobs):
                        print("Reached end of results")
                        break
                    
                    page += 1
                    
                    # Safety check to avoid infinite loop
                    if page > 50:  # Max 50 pages
                        print("Reached maximum page limit")
                        break
                        
                except json.JSONDecodeError:
                    print("Jobs response not JSON:", jobs_response.text[:200])
                    break
            else:
                print(f"Jobs API failed: {jobs_response.status_code}")
                print("Error response:", jobs_response.text[:300])
                break
    
        if all_jobs:
            print(f"\nSuccessfully scraped {len(all_jobs)} jobs for '{search_query}'")
            return all_jobs
        else:
            print("No jobs found")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []

def save_jobs_to_json(jobs, filename):
    """
    Save job data to JSON file
    
    Args:
        jobs (list): List of job dictionaries
        filename (str): Output filename
    """
    if jobs:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(jobs)} jobs to {filename}")
    else:
        print("No jobs to save")

if __name__ == "__main__":
    # Example usage
    search_term = input("Enter search term (e.g., 'Data Scientist', 'Software Engineer'): ")
    
    # Scrape jobs
    jobs = scrape_hiring_cafe_jobs(search_term)
    
    if jobs:
        # Save to JSON file
        filename = f"{search_term.lower().replace(' ', '_')}_jobs.json"
        save_jobs_to_json(jobs, filename)
        
        print(f"\nScraping completed! Found {len(jobs)} jobs for '{search_term}'")
        print(f"Data saved to: {filename}")
        
        # Show sample job data structure
        if len(jobs) > 0 and isinstance(jobs[0], dict):
            sample_keys = list(jobs[0].keys())
            print(f"Job data includes: {', '.join(sample_keys[:10])}")
    else:
        print("Scraping unsuccessful. No jobs were found.")