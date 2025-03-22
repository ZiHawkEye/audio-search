## System Architecture

### Overview
The audio-search application follows a client-server architecture with the following main components:

```mermaid
graph TB
    subgraph Frontend
        AC[AudioPreview Component]
        SC[SearchBar Component]
    end

    subgraph Backend
        API[Flask API Server]
    end

    subgraph External Services
        W[Whisper Model]
    end

    subgraph Database
        DB[(SQLite Database)]
    end

    AC --> |Audio Upload| API
    SC --> |Search Queries, HTTP Requests| API
    API --> |Transcription| W
    API <--> |CRUD Operations| DB
```

### Component Details

#### Frontend Layer
- **Technology**: Vue.js
- **Key Components**:
  - AudioPreview: Uploads audio files
  - SearchBar: Searches for transcriptions by file name

#### Backend Layer
- **Technology**: Flask (Python)
- **Key Components**:
  - RESTful API endpoints
  - OpenAI Whisper for transcription
- **API Endpoints**:
  - `/transcribe`: Audio file transcription
  - `/search`: Text search functionality
  - `/transcriptions`: Retrieval of stored transcriptions
  - `/delete`: Delete transcriptions

#### Database Layer
- **Technology**: SQLite
- **Schema**:
  - Transcriptions table:
    - Audio file name
    - Transcribed content
    - Timestamp of creation

#### External Services
- OpenAI Whisper (running locally)
  - Used for audio transcription
  - Base model implementation
