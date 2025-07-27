# AirLogger Standalone

A modern web application for aircraft flight tracking and financial analysis, featuring automated development feedback loops with MCP servers.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Backend API running on `localhost:5000`

### Installation
```bash
git clone <repository>
cd airlogger-standalone
npm install
```

### Development
```bash
# Start the dev server
npm run dev

# Open http://localhost:3010
```

## 📊 Features

### Flight Tracking
- **Dashboard**: Real-time flight summary with key metrics
- **Flight History**: Detailed flight logs with revenue calculations
- **Financial Settings**: Configure revenue and cost parameters
- **Breakeven Analysis**: Track progress toward profitability

### Automated Development Feedback Loop
- **Sequential Thinking**: AI-powered change analysis
- **Visual Testing**: Automated UI state capture
- **Context Persistence**: Long-term memory of decisions
- **Validation Workflow**: Structured change implementation

## 🛠 Development Workflow

### Standard Development
```bash
# Start dev server
npm run dev

# Make changes to components
# Browser auto-reloads
```

### Feedback Loop Development
```bash
# 1. Create a change request
npm run feedback:new "Feature Name" "Description"

# 2. Capture current UI state
npm run feedback:capture

# 3. Make your changes
# Edit components, styles, etc.

# 4. Validate changes
npm run feedback validate <change-id>

# 5. List all requests
npm run feedback:list
```

## 🎯 Example Workflow

Try the automated feedback loop:

```bash
# Create a change request for dark mode
npm run feedback:new "Dark Mode Toggle" "Add dark mode support"

# Capture current state
npm run feedback:capture

# View the analysis
npm run feedback:list

# After making changes, validate them
npm run feedback validate 8kmwd5l8y
```

## 📚 Documentation

- [Development Feedback Loop Guide](./DEVELOPMENT_FEEDBACK_LOOP.md)
- Full system architecture and MCP server setup

## 🤝 Ready to Use

The application is running at **http://localhost:3010** with:
- ✅ Complete flight dashboard
- ✅ Financial tracking and breakeven analysis  
- ✅ Automated development feedback loop
- ✅ MCP server integration for AI-powered development

Start using the feedback loop system to make systematic improvements to the AirLogger interface!