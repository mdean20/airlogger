"""
API endpoints for AirLogger backend.
"""
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timezone, timedelta
import logging
from sqlalchemy.exc import SQLAlchemyError
from app import Session
from app.models import FlightRecord, FinancialSettings
from app.services.flightaware import FlightAwareClient

logger = logging.getLogger(__name__)

# Create Blueprint
api_bp = Blueprint('api', __name__)

# Default values
DEFAULT_TAIL_NUMBER = "N593EH"


def get_db_session():
    """Get database session."""
    return Session()


@api_bp.route('/refresh_data', methods=['POST'])
def refresh_data():
    """
    Trigger a refresh of flight data from FlightAware.
    Fetches last 90 days of data for the default tail number.
    """
    session = get_db_session()
    try:
        # Calculate date range (last 90 days)
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=90)
        
        logger.info(f"Starting data refresh for {DEFAULT_TAIL_NUMBER}")
        
        # Initialize FlightAware client
        try:
            client = FlightAwareClient()
        except ValueError as e:
            logger.error(f"Failed to initialize FlightAware client: {e}")
            return jsonify({"error": "FlightAware API configuration error"}), 500
        
        # Fetch data from FlightAware
        raw_flights = client.fetch_aircraft_history(DEFAULT_TAIL_NUMBER, start_date, end_date)
        
        if not raw_flights:
            return jsonify({"message": "No new data fetched from FlightAware or API error."}), 200
        
        # Process flight data
        processed_flights = client.process_flight_data(raw_flights)
        
        # Store in database (avoiding duplicates)
        new_count = 0
        for flight in processed_flights:
            existing = session.query(FlightRecord).filter_by(id=flight.id).first()
            if not existing:
                session.add(flight)
                new_count += 1
            else:
                logger.debug(f"Flight {flight.id} already exists, skipping")
        
        session.commit()
        
        message = f"Data refreshed successfully. Stored {new_count} new flights."
        logger.info(message)
        return jsonify({"message": message}), 200
        
    except Exception as e:
        session.rollback()
        logger.error(f"Error during data refresh: {e}", exc_info=True)
        return jsonify({"error": "Failed to refresh data", "details": str(e)}), 500
    finally:
        session.close()


@api_bp.route('/flights', methods=['GET'])
def get_flights():
    """
    Retrieve flight records for a specified date range.
    Query parameters:
    - tail_number (optional, defaults to N593EH)
    - start_date (required, YYYY-MM-DD)
    - end_date (required, YYYY-MM-DD)
    """
    # Parse query parameters
    tail_number = request.args.get('tail_number', DEFAULT_TAIL_NUMBER)
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    # Validate required parameters
    if not (start_date_str and end_date_str):
        return jsonify({"error": "start_date and end_date are required"}), 400
    
    # Parse dates
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        # Make end_date inclusive (end of day)
        end_date = (datetime.strptime(end_date_str, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)).replace(tzinfo=timezone.utc)
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    session = get_db_session()
    try:
        # Get financial settings for revenue calculation
        settings = FinancialSettings.get_or_create_default(session)
        
        # Query flights
        flights = session.query(FlightRecord).filter(
            FlightRecord.tail_number == tail_number,
            FlightRecord.departure_time_utc >= start_date,
            FlightRecord.departure_time_utc <= end_date
        ).order_by(FlightRecord.departure_time_utc).all()
        
        # Convert to dictionaries with revenue calculation
        flight_list = [flight.to_dict(revenue_per_hour=settings.revenue_per_hour) for flight in flights]
        
        return jsonify(flight_list), 200
        
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_flights: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        session.close()


@api_bp.route('/summary', methods=['GET'])
def get_summary():
    """
    Calculate and return summary statistics for a date range.
    Query parameters:
    - tail_number (optional, defaults to N593EH)
    - start_date (required, YYYY-MM-DD)
    - end_date (required, YYYY-MM-DD)
    """
    # Parse query parameters
    tail_number = request.args.get('tail_number', DEFAULT_TAIL_NUMBER)
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    # Validate required parameters
    if not (start_date_str and end_date_str):
        return jsonify({"error": "start_date and end_date are required"}), 400
    
    # Parse dates
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        end_date = (datetime.strptime(end_date_str, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)).replace(tzinfo=timezone.utc)
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    session = get_db_session()
    try:
        # Get financial settings
        settings = FinancialSettings.get_or_create_default(session)
        
        # Query flights
        flights = session.query(FlightRecord).filter(
            FlightRecord.tail_number == tail_number,
            FlightRecord.departure_time_utc >= start_date,
            FlightRecord.departure_time_utc <= end_date
        ).all()
        
        # Calculate totals with Hobbs time (add 15 minutes per flight)
        total_hobbs_minutes = sum(f.flight_duration_minutes + 15 for f in flights)
        
        # Calculate billable hours (round up each flight to nearest 0.1 hour)
        total_billable_hours = 0.0
        for flight in flights:
            hobbs_minutes = flight.flight_duration_minutes + 15
            hobbs_hours = hobbs_minutes / 60.0
            # Round up to nearest 0.1 hour (6 minutes)
            billable_hours = round(hobbs_hours * 10 + 0.49) / 10
            total_billable_hours += billable_hours
        
        # Financial calculations based on billable hours
        total_revenue = round(total_billable_hours * settings.revenue_per_hour, 2)
        total_variable_costs = round(total_billable_hours * settings.variable_cost_per_hour, 2)
        
        # Fixed costs proportional to period
        days_in_period = (end_date - start_date).days + 1
        avg_days_in_month = 30.44  # Average days per month
        total_fixed_costs = round((settings.monthly_fixed_costs / avg_days_in_month) * days_in_period, 2)
        
        net_profit = round(total_revenue - total_variable_costs - total_fixed_costs, 2)
        
        # Breakeven calculations
        # Breakeven revenue = Fixed costs + (Variable cost per hour * Hours needed)
        # Since revenue per hour > variable cost per hour, we can calculate hours needed
        profit_margin_per_hour = settings.revenue_per_hour - settings.variable_cost_per_hour
        
        if profit_margin_per_hour > 0:
            # Hours needed to cover fixed costs
            breakeven_hours = total_fixed_costs / profit_margin_per_hour
            # Round up to nearest 0.1 hour for billing purposes
            breakeven_billable_hours = round(breakeven_hours * 10 + 0.49) / 10
            breakeven_revenue = round(breakeven_billable_hours * settings.revenue_per_hour, 2)
            
            # Additional hours needed from current position
            additional_hours_needed = max(0, breakeven_billable_hours - total_billable_hours)
            additional_revenue_needed = round(max(0, breakeven_revenue - total_revenue), 2)
        else:
            # Cannot break even if variable costs >= revenue
            breakeven_billable_hours = None
            breakeven_revenue = None
            additional_hours_needed = None
            additional_revenue_needed = None
        
        summary = {
            "period": "Custom",
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
            "totalFlightMinutes": sum(f.flight_duration_minutes for f in flights),
            "totalHobbsMinutes": total_hobbs_minutes,
            "totalBillableHours": round(total_billable_hours, 2),
            "totalRevenue": total_revenue,
            "totalFixedCosts": total_fixed_costs,
            "totalVariableCosts": total_variable_costs,
            "netProfit": net_profit,
            "breakeven": {
                "revenueNeeded": breakeven_revenue,
                "hoursNeeded": breakeven_billable_hours,
                "additionalRevenueNeeded": additional_revenue_needed,
                "additionalHoursNeeded": round(additional_hours_needed, 2) if additional_hours_needed is not None else None,
                "profitMarginPerHour": round(profit_margin_per_hour, 2)
            }
        }
        
        return jsonify(summary), 200
        
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_summary: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        session.close()


@api_bp.route('/financial-settings', methods=['GET'])
def get_financial_settings():
    """Retrieve current financial settings."""
    session = get_db_session()
    try:
        settings = FinancialSettings.get_or_create_default(session)
        return jsonify(settings.to_dict()), 200
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_financial_settings: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        session.close()


@api_bp.route('/financial-settings', methods=['PUT'])
def update_financial_settings():
    """Update financial settings."""
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['revenue_per_hour', 'monthly_fixed_costs', 'variable_cost_per_hour']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Validate numeric values
        try:
            float(data[field])
        except (TypeError, ValueError):
            return jsonify({"error": f"Invalid value for {field}: must be a number"}), 400
    
    session = get_db_session()
    try:
        # Get or create settings
        settings = FinancialSettings.get_or_create_default(session)
        
        # Update values
        settings.revenue_per_hour = float(data['revenue_per_hour'])
        settings.monthly_fixed_costs = float(data['monthly_fixed_costs'])
        settings.variable_cost_per_hour = float(data['variable_cost_per_hour'])
        
        session.commit()
        
        return jsonify(settings.to_dict()), 200
        
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error in update_financial_settings: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        session.close()