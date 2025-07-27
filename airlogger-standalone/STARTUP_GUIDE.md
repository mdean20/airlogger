# AirLogger Standalone - Startup Guide

## 🚀 Quick Start Commands

### 1. Ensure Dependencies are Installed
```bash
npm install
```

### 2. Start the Development Server
```bash
npm run dev
```
- **Runs on**: http://localhost:3010
- **Note**: Command will show "Ready" then stay running (this is normal)
- **To stop**: Press `Ctrl+C`

### 3. Start in Background (Optional)
```bash
npm run dev &
```

## 🛠 Troubleshooting

### Error: "sh: next: command not found"
**Solution**: Package.json has been updated to use `npx`. Run:
```bash
npm install
npm run dev
```

### Error: "address already in use :::3010"
**Solution**: Kill the existing process:
```bash
lsof -ti:3010 | xargs kill -9
npm run dev
```

### Error: "Cannot find module dev-feedback-loop.js"
**Solution**: Ensure you're in the correct directory:
```bash
cd /Users/mauricedean/Library/CloudStorage/Dropbox/Code/github/airlogger/airlogger-standalone
ls scripts/  # Should show dev-feedback-loop.js
npm run feedback:list
```

## 📋 Development Workflow

### Start Development Session
```bash
# Terminal 1: Start dev server
npm run dev

# Terminal 2: Use for development commands
npm run feedback:new "Feature Name"
npm run feedback:capture
npm run feedback:list
```

### Quick Health Check
```bash
# Check if frontend is running
curl -I http://localhost:3010

# Check if backend is running  
curl -I http://localhost:5000/api/financial-settings

# List recent change requests
npm run feedback:list
```

## ✅ Expected Output

### Successful Startup
```bash
npm run dev

> airlogger-standalone@0.1.0 dev
> npx next dev -p 3010

   ▲ Next.js 15.4.4
   - Local:        http://localhost:3010
   - Network:      http://169.254.2.82:3010
   - Environments: .env.local

 ✓ Starting...
 ✓ Ready in 1109ms
```

### Working Feedback Loop
```bash
npm run feedback:list

📚 Recent Change Requests:
   ⏳ [77nrhgdl0] Test ability to connect with standalone website and fix issues detected (ready-for-implementation)
   ⏳ [8kmwd5l8y] Dark Mode Toggle (ready-for-implementation)
```

## 🎯 Ready to Develop!

Once you see "✓ Ready", the AirLogger application is running at:
- **Frontend**: http://localhost:3010
- **Backend**: http://localhost:5000 (should already be running)
- **Feedback Loop**: Ready to track changes

The system is now ready for systematic frontend development with automated feedback loops!