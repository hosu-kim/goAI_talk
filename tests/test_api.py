#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime, timedelta
import os
import sys

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

def test_api_connection():
    """Test API connection and data retrieval"""
    
    # API configuration
    base_url = config.API_FOOTBALL_URL
    headers = {
        "x-apisports-key": config.API_FOOTBALL_KEY
    }

    # Get yesterday's date
    yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    print(f"\n{'='*60}")
    print("API Connection Test")
    print(f"{'='*60}")
    print(f"Current UTC Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Testing Date: {yesterday}")
    print(f"API URL: {base_url}")
    print(f"Headers: {headers}")  # API 키 마스킹 처리
    
    # Test endpoint
    endpoints = [
        {
            "name": "Fixtures",
            "url": f"{base_url}/fixtures",
            "params": {"date": yesterday, "status": "FT-AET-PEN"}
        },
        {
            "name": "Status",
            "url": f"{base_url}/status",
            "params": {}
        }
    ]
    
    for endpoint in endpoints:
        print(f"\n{'-'*60}")
        print(f"Testing Endpoint: {endpoint['name']}")
        print(f"URL: {endpoint['url']}")
        print(f"Parameters: {endpoint['params']}")
        
        try:
            response = requests.get(
                endpoint['url'],
                headers=headers,
                params=endpoint['params']
            )
            
            print(f"\nResponse Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                data = response.json()
                print("\nResponse Data Structure:")
                print(f"Keys in response: {list(data.keys())}")
                
                if 'response' in data:
                    matches = data['response']
                    print(f"\nNumber of matches: {len(matches)}")
                    
                    if matches:
                        print("\nFirst match details:")
                        print(json.dumps(matches[0], indent=2))
                    else:
                        print("No matches found for this date")
                
                if 'errors' in data:
                    print("\nAPI Errors:")
                    print(json.dumps(data['errors'], indent=2))
                    
            else:
                print("\nError Response:")
                print(response.text)
                
        except requests.exceptions.RequestException as e:
            print(f"\nRequest Error: {str(e)}")
        except json.JSONDecodeError as e:
            print(f"\nJSON Parsing Error: {str(e)}")
        except Exception as e:
            print(f"\nUnexpected Error: {str(e)}")

if __name__ == "__main__":
    try:
        print("\nStarting API test...")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Python path: {sys.path}")
        test_api_connection()
    except Exception as e:
        print(f"\nTest failed with error: {str(e)}")
