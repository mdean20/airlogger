# AirLogger Development Feedback Loop

An automated system for frontend development that uses MCP servers to analyze, track, and validate UI changes.

## Overview

This system creates a continuous improvement cycle where each change is:
1. **Analyzed** using Sequential Thinking to break down requirements
2. **Tracked** with persistent context storage
3. **Validated** using visual testing with Puppeteer

## Setup

### 1. MCP Server Configuration

The project includes a `claude_desktop_config.json` that configures these MCP servers:
- **Sequential Thinking**: Analyzes change requests and breaks them into steps
- **Puppeteer**: Captures UI state and performs visual testing  
- **Filesystem**: Manages project files and context storage

### 2. Available Commands

```bash
# Create a new change request
npm run feedback:new "Dark Mode Toggle"
npm run feedback:new "Responsive Navigation" "Make nav work on mobile"

# Capture current UI state
npm run feedback:capture

# List all change requests
npm run feedback:list

# Validate implemented changes
npm run feedback validate <change-id>

# Start development monitoring
npm run feedback:monitor
```

## Example Workflow

### 1. Create a Change Request
```bash
npm run feedback:new "Dark Mode Toggle"
```
**Output:**
```
🚀 Creating change request: "Dark Mode Toggle"
📋 Analysis complete. 5 steps identified:
   1. Update color scheme variables
   2. Add theme toggle component
   3. Implement theme persistence
   4. Update all UI components for dark mode
   5. Test accessibility in both modes
```

### 2. Capture UI State (Before)
```bash
npm run feedback:capture
```
**Output:**
```
📷 Capturing current UI state...
✅ UI state captured: screenshots/state-2025-07-26T16-30-00.png
```

### 3. Make Your Changes
Edit your components, styles, etc. The dev server auto-reloads.

### 4. Validate Changes
```bash
npm run feedback validate abc123def
```
**Output:**
```
🔍 Validating changes for request abc123def...
📷 Capturing current UI state...
✅ Validation complete!
   ✓ UI elements are properly responsive
   ✓ Color contrast meets accessibility standards
   ✓ Interactive elements have proper hover states
```

## Context Storage

The system maintains context in the `.dev-context/` directory:

```
.dev-context/
├── change-abc123def.json    # Change request with analysis steps
├── change-xyz789ghi.json    # Another change request
└── ...

screenshots/
├── state-2025-07-26T16-30-00.png    # UI screenshots
├── state-2025-07-26T16-30-00.json   # Metadata
└── ...
```

## Change Request Structure

Each change request includes:

```json
{
  "id": "abc123def",
  "title": "Dark Mode Toggle",
  "description": "Add dark mode support to the application",
  "timestamp": "2025-07-26T16:30:00.000Z",
  "status": "completed",
  "steps": [
    {
      "title": "Update color scheme variables",
      "type": "styling",
      "priority": "high"
    }
  ],
  "validation": {
    "timestamp": "2025-07-26T17:00:00.000Z",
    "passed": true,
    "issues": [],
    "improvements": [
      "UI elements are properly responsive"
    ]
  }
}
```

## MCP Server Integration

### Sequential Thinking Server
- Analyzes change requests using AI reasoning
- Breaks complex changes into actionable steps
- Identifies dependencies and priorities

### Puppeteer Server  
- Captures high-resolution screenshots
- Performs automated UI testing
- Validates responsive behavior
- Checks accessibility compliance

### Context7 Server (Future)
- Maintains long-term memory of decisions
- Learns from past implementations
- Suggests improvements based on patterns

## Common Change Patterns

The system recognizes common patterns and provides tailored analysis:

### Dark Mode
- Update color scheme variables
- Add theme toggle component
- Implement theme persistence
- Update all UI components
- Test accessibility

### Responsive Design
- Analyze current breakpoints
- Update CSS layouts
- Test on multiple screen sizes
- Optimize touch interactions

### Performance
- Analyze bundle size
- Implement code splitting
- Optimize images and assets
- Add performance monitoring

## Benefits

1. **Systematic Approach**: Every change follows a structured process
2. **Visual Validation**: Screenshots ensure UI changes work as expected
3. **Knowledge Retention**: Context is preserved for future reference
4. **Automated Testing**: Reduces manual validation effort
5. **Continuous Improvement**: Learn from past implementations

## Future Enhancements

- **Real-time Visual Diff**: Compare before/after screenshots
- **Automated Accessibility Testing**: WCAG compliance checks
- **Performance Metrics**: Bundle size and load time tracking
- **Integration Testing**: API and component interaction validation
- **Design System Compliance**: Ensure components follow design standards

## Troubleshooting

### MCP Servers Not Found
```bash
# Install MCP servers globally
npm install -g @modelcontextprotocol/server-sequential-thinking
npm install -g @modelcontextprotocol/server-puppeteer
npm install -g @modelcontextprotocol/server-filesystem
```

### Permission Issues
```bash
# Make scripts executable
chmod +x scripts/dev-feedback-loop.js
```

### Port Conflicts
The system expects the dev server on `localhost:3010`. If using a different port, update the script configuration.