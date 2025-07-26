#!/usr/bin/env python3
"""
Test script to verify API endpoints are working.
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"

def test_refresh_data():
    """Test the refresh data endpoint."""
    print("1. Testing /api/refresh_data endpoint...")
    
    try:
        response = requests.post(f"{BASE_URL}/refresh_data")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Success: {data['message']}")
        else:
            print(f"   ✗ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("   ✗ Error: Cannot connect to server. Is it running?")
        return False
    
    return response.status_code == 200

def test_get_flights():
    """Test the get flights endpoint."""
    print("\n2. Testing /api/flights endpoint...")
    
    # Get flights for last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    params = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d")
    }
    
    response = requests.get(f"{BASE_URL}/flights", params=params)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        flights = response.json()
        print(f"   ✓ Found {len(flights)} flights")
        
        if flights:
            flight = flights[0]
            print(f"\n   Most recent flight:")
            print(f"     {flight['departureAirport']} → {flight['arrivalAirport']}")
            print(f"     Duration: {flight['flightDurationMinutes']} minutes")
            print(f"     Revenue: ${flight['estimatedRevenue']}")
    else:
        print(f"   ✗ Error: {response.text}")
    
    return response.status_code == 200

def test_get_summary():
    """Test the summary endpoint."""
    print("\n3. Testing /api/summary endpoint...")
    
    # Get summary for last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    params = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d")
    }
    
    response = requests.get(f"{BASE_URL}/summary", params=params)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        summary = response.json()
        print(f"   ✓ Summary for {summary['period']} period:")
        print(f"     Total Hours: {summary['totalFlightHours']}")
        print(f"     Revenue: ${summary['totalRevenue']}")
        print(f"     Fixed Costs: ${summary['totalFixedCosts']}")
        print(f"     Variable Costs: ${summary['totalVariableCosts']}")
        print(f"     Net Profit: ${summary['netProfit']}")
    else:
        print(f"   ✗ Error: {response.text}")
    
    return response.status_code == 200

def test_financial_settings():
    """Test financial settings endpoints."""
    print("\n4. Testing /api/financial-settings endpoints...")
    
    # Get current settings
    response = requests.get(f"{BASE_URL}/financial-settings")
    print(f"   GET Status: {response.status_code}")
    
    if response.status_code == 200:
        settings = response.json()
        print(f"   ✓ Current settings:")
        print(f"     Revenue/hour: ${settings['revenue_per_hour']}")
        print(f"     Fixed costs/month: ${settings['monthly_fixed_costs']}")
        print(f"     Variable costs/hour: ${settings['variable_cost_per_hour']}")
    
    return response.status_code == 200

def main():
    """Run all tests."""
    print("Testing AirLogger API endpoints...")
    print("Make sure the Flask server is running on http://localhost:5000")
    print("-" * 60)
    
    # Run tests
    tests = [
        test_refresh_data,
        test_get_flights,
        test_get_summary,
        test_financial_settings
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"   ✗ Unexpected error: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")

if __name__ == "__main__":
    main()