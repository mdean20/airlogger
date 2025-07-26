#!/usr/bin/env python3
"""
Test script to verify FlightAware API connection.
"""
import os
import sys
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

from app.services.flightaware import FlightAwareClient

def test_api_connection():
    """Test the FlightAware API connection."""
    print("Testing FlightAware API connection...")
    
    try:
        # Test with raw requests first
        import requests
        
        api_key = os.getenv("FLIGHTAWARE_API_KEY")
        if not api_key:
            print("✗ No API key found in environment")
            return False
        
        print(f"✓ API Key found: {api_key[:10]}...")
        
        # Try a simpler endpoint first - check if registration exists
        base_url = "https://aeroapi.flightaware.com/aeroapi"
        headers = {"x-apikey": api_key}
        
        # Try the flights endpoint with registration
        url = f"{base_url}/flights/N593EH"
        print(f"\nTrying endpoint: {url}")
        
        response = requests.get(url, headers=headers)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            flights = data.get("flights", [])
            print(f"\n✓ Successfully connected! Found {len(flights)} recent flights")
            
            if flights:
                # Find first non-cancelled flight
                non_cancelled = [f for f in flights if not f.get('cancelled', False)]
                
                if non_cancelled:
                    flight = non_cancelled[0]
                    print("\nFirst non-cancelled flight:")
                else:
                    flight = flights[0]
                    print("\nAll flights are cancelled. First flight:")
                
                print(f"  Flight ID: {flight.get('fa_flight_id', 'N/A')}")
                print(f"  Origin: {flight.get('origin', {}).get('code', 'N/A')}")
                print(f"  Destination: {flight.get('destination', {}).get('code', 'N/A')}")
                print(f"  Cancelled: {flight.get('cancelled', False)}")
                print(f"  Departure: {flight.get('actual_off') or flight.get('scheduled_off', 'N/A')}")
                print(f"  Arrival: {flight.get('actual_on') or flight.get('scheduled_on', 'N/A')}")
                
                # Summary of all flights
                print(f"\nTotal flights: {len(flights)}")
                print(f"Cancelled: {sum(1 for f in flights if f.get('cancelled', False))}")
                print(f"Completed: {sum(1 for f in flights if not f.get('cancelled', False))}")
        else:
            print(f"\n✗ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
            # Try a different endpoint
            print("\nTrying history endpoint...")
            end_date = datetime.now(timezone.utc)
            start_date = end_date - timedelta(days=30)
            
            # Initialize client
            client = FlightAwareClient()
            flights = client.fetch_aircraft_history("N593EH", start_date, end_date)
            
            if flights:
                print(f"✓ Found {len(flights)} flights in last 30 days")
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_api_connection()
    sys.exit(0 if success else 1)