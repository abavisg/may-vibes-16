# Debate Day Web UI

A Flutter web UI for the Debate Day project. This application allows users to watch AI agents debate topics in real-time.

## Features

- Create debates on any topic
- Watch AI agents debate in real-time
- Pro and Con positions presented visually
- Moderated debate format
- Multiple rounds of discussion

## Recent Updates

- Added support for System role messages
- Fixed issue with displaying the Pro agent as active when it's their turn
- Fixed issue with API debate ID handling to ensure correct polling and message sending
- Improved error handling for API communication
- Added visual indicators for active speakers
- Fixed linter warnings throughout the codebase
- Improved logging with a centralized _log function

## Getting Started

1. Make sure the backend API server is running (usually at http://localhost:8000)
2. Run the Flutter app:

```bash
cd debate_day/flutter_ui/debate_day_web
flutter run -d web-server --web-port 8080
```

3. Navigate to http://localhost:8080 in your browser

## API Connection

The app will automatically connect to the debate API at http://localhost:8000/api. If you need to use a different endpoint, you can modify the `baseUrl` in the ApiService class.

## Troubleshooting

- If the app shows "API server appears to be offline", make sure the backend server is running
- If messages aren't updating, check the API logs for potential errors
- If agents are not responding, ensure the backend agent services are running

## Architecture

This application uses:

- **Flutter for Web**: Cross-platform UI framework
- **Provider**: Simple state management
- **HTTP**: REST API communication with the Python backend
- **Extensive Error Handling**: Robust error catching and logging for debugging

## Project Structure

```
lib/
├── main.dart                // App entry point and theming
├── pages/
│   └── debate_page.dart     // Main vertical split UI
├── widgets/
│   ├── avatar_widget.dart   // Agent avatar display
│   ├── message_bubble.dart  // Message display widget
│   └── toolbar.dart         // Top toolbar with debate controls
├── models/
│   └── debate_models.dart   // Data models for debate entities
└── services/
    └── api_service.dart     // REST API client for backend
```

## Error Handling & Debugging

This application includes comprehensive error handling and logging:

- **Global Error Handling**: Catches and logs all Flutter framework errors
- **Zone-based Error Capture**: Captures errors outside Flutter's scope
- **API Response Validation**: Validates all API responses for required fields
- **Null Safety**: Careful handling of nullable values to prevent null errors
- **API Availability Check**: Checks if the API server is available and shows warnings if not
- **Fallback Mechanisms**: Can generate local IDs and default values when API responses are incomplete
- **Debug Logging**: Extensive logging when in debug mode for:
  - API requests and responses
  - Data parsing and validation
  - UI state changes
  - Error details with stack traces

Debug logs use emoji prefixes for easy identification:
- 🚀 - Application startup/initialization
- 📡 - API operations
- 📦 - Data parsing/model creation
- ⚠️ - Warnings (non-fatal issues)
- ⛔ - Errors
- 🔴 - Fatal/uncaught errors
- ✅ - Successful operations
- 🔄 - Background operations (polling)

## Setup & Running

### Prerequisites

- Flutter SDK (latest stable)
- Running Debate Day backend (Python/FastAPI)

### Development

1. Make sure the Debate Day backend server is running at `http://localhost:8000`
2. Run the Flutter web app:

```bash
cd debate_day/flutter_ui/debate_day_web
flutter run -d chrome
```

### Building for Production

```bash
flutter build web
```

The output will be in `build/web` directory, which can be deployed to any web server.

## Backend API Integration

The application communicates with the Debate Day backend API at:

- `POST /api/start` - Start a new debate
- `GET /api/context/{debate_id}` - Get message history
- `GET /api/turn/{debate_id}` - Check whose turn it is
- `GET /api/status/{debate_id}` - Check debate status
- `GET /api/debate/{debate_id}` - Get detailed debate info

The application polls these endpoints every 5 seconds to keep the UI updated with the latest debate state.
