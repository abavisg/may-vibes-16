# Debate Day 2.0 - Flutter Web UI

This is the Flutter web implementation for the Debate Day 2.0 multi-agent debate simulation system.

## Features

- Modern, responsive web UI for the Debate Day backend
- Real-time display of debate messages between Pro and Con agents
- Visual indication of which agent is currently speaking
- Debate configuration options (topic, number of rounds)
- Verdict display when a debate is complete

## Architecture

This application uses:

- **Flutter for Web**: Cross-platform UI framework
- **Provider**: Simple state management
- **HTTP**: REST API communication with the Python backend

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
