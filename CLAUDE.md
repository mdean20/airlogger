# Aircraft Tracker Implementation Notes

## Project Overview
Aircraft tracking application for N593EH with Python Flask backend on M2 Mac Mini and iOS SwiftUI frontend.

## Key Commands
- **Backend**: `python app.py` (runs on port 5000)
- **iOS**: Build and run in Xcode
- **Database**: SQLite at `flight_tracker.db`

## MCP Server Integration for Frontend Development

### Automated Development Feedback Loop

The project can leverage MCP (Model Context Protocol) servers to create an intelligent feedback loop for frontend development. This approach enables automated UI validation, persistent decision tracking, and continuous improvement.

### Workflow Implementation

#### 1. Change Request Initiation
```bash
node scripts/dev-feedback-loop.js new "Dark Mode Toggle"
```

#### 2. Automated Processing Pipeline
The system orchestrates three MCP servers:

**Sequential Thinking Server**
- Analyzes the change request
- Breaks down implementation into logical steps
- Identifies dependencies and potential impacts
- Creates an execution plan

**Puppeteer Server**
- Captures current UI state before changes
- Takes screenshots for visual comparison
- Runs automated interaction tests
- Validates UI changes against requirements

**Context7 Server**
- Stores implementation context and decisions
- Maintains knowledge base of patterns
- Tracks change history
- Provides context for future similar changes

#### 3. Development Integration
- Changes are made while dev server auto-reloads
- Real-time validation against captured baseline
- Automated testing runs on each change
- Visual regression testing ensures UI consistency

#### 4. Validation & Storage
- Visual testing confirms changes meet requirements
- Successful patterns are stored for reuse
- Failed attempts are logged with reasons
- Decision tree builds over time

### Benefits of MCP Server Integration

1. **Continuous Learning**: Each change builds on previous knowledge
2. **Automated Validation**: Visual and functional testing without manual intervention
3. **Pattern Recognition**: Common UI patterns are identified and reused
4. **Reduced Errors**: Automated testing catches issues before deployment
5. **Documentation**: All decisions and changes are automatically documented

### Implementation Example for Aircraft Tracker

For the iOS frontend development:

```javascript
// Example: Adding flight duration display feature
node scripts/dev-feedback-loop.js new "Add flight duration in hours:minutes format"

// Sequential Thinking would:
// 1. Identify where duration is displayed (FlightListView)
// 2. Plan formatter implementation
// 3. Consider localization needs

// Puppeteer would:
// 1. Capture current flight list display
// 2. Monitor changes during implementation
// 3. Validate new format displays correctly

// Context7 would:
// 1. Store the formatting decision
// 2. Remember this pattern for future time displays
// 3. Link to similar implementations
```

### Setup Requirements

1. Install MCP servers:
   - @modelcontextprotocol/server-sequential-thinking
   - @modelcontextprotocol/server-puppeteer
   - @modelcontextprotocol/server-context7

2. Configure MCP in Claude desktop settings

3. Create feedback loop script at `scripts/dev-feedback-loop.js`

4. Set up visual testing baseline

### Future Enhancements

- Integrate with iOS Simulator for native app testing
- Add performance monitoring to feedback loop
- Create UI component library from learned patterns
- Implement A/B testing for UI changes

## Additional Implementation Notes

### API Endpoints
- `POST /api/refresh_data` - Sync with FlightAware
- `GET /api/flights?tail_number=N593EH&start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
- `GET /api/summary?tail_number=N593EH&start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`

### Environment Variables
```bash
FLIGHTAWARE_API_KEY=your_key_here
FLASK_PORT=5000
```

### API Keys
- FlightAware API Key: `yVL1HkC4WkfqAgh1VCBmRztDSAGWAy5o`

### Tailscale Configuration
- Backend: Bind to `0.0.0.0:5000`
- iOS: Update `baseURL` in BackendService with Tailscale IP
- Example: `http://100.x.x.x:5000`

### Testing Checklist
- [ ] FlightAware API connection
- [ ] Database write/read operations
- [ ] iOS to backend connectivity via Tailscale
- [ ] Date range queries
- [ ] Financial calculations
- [ ] Error handling for network failures

### FlightAware (AeroAPI) Configuration
- Endpoint URL: `https://aeroapi.flightaware.com/aeroapi`
- Pricing Model:
  - Revenue: $299/hour
  - Fixed Monthly Cost: $1200/month
  - Variable Cost: $80 per usage