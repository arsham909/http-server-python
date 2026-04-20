# HTTP/1.1 Server Implementation

A production-ready HTTP/1.1 server built from scratch in Python, demonstrating core networking concepts and protocol implementation.

## Features

### Core HTTP Functionality
- **HTTP/1.1 Protocol Compliance** - Full request/response cycle following RFC 2616
- **Concurrent Request Handling** - Multi-threaded architecture supporting simultaneous client connections
- **GET & POST Methods** - Complete support for standard HTTP methods with proper status codes
- **File Operations** - Serve static files and handle file uploads with path validation
- **Content Encoding** - Gzip compression support based on client Accept-Encoding headers
- **Connection Management** - Proper handling of persistent and close connections

### Request Processing
- Request line parsing (method, path, version)
- Header extraction and processing (User-Agent, Accept-Encoding, Content-Length, etc.)
- Body handling for POST requests
- Proper status codes (200, 201, 400, 404, 405, 500)

## Architecture

```
┌─────────────────────────────────────────┐
│        Socket Server (Threaded)         │
├─────────────────────────────────────────┤
│                                         │
│  ┌────────────────────────────────┐   │
│  │  Request Parser                │   │
│  │  • Header Processing           │   │
│  │  • Method Routing              │   │
│  ├────────────────────────────────┤   │
│  │  Request Handlers              │   │
│  │  • GET /echo/{string}          │   │
│  │  • GET /user-agent             │   │
│  │  • GET /files/{filename}       │   │
│  │  • POST /files/{filename}      │   │
│  └────────────────────────────────┘   │
│                                         │
│  ┌────────────────────────────────┐   │
│  │  Response Builder              │   │
│  │  • Status Line Generation      │   │
│  │  • Header Composition          │   │
│  │  • Content Encoding (gzip)     │   │
│  └────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

## Usage

### Starting the Server

```bash
# Default: runs on localhost:4221, serves current directory
python app/main.py

# Specify a directory to serve
python app/main.py localhost 4221 /path/to/files
```

### API Endpoints

**Echo Service**
```bash
GET /echo/hello
# Returns: hello (200 OK)
```

**User-Agent Detection**
```bash
GET /user-agent
# Returns: client's user-agent string (200 OK)
```

**File Serving**
```bash
GET /files/document.txt
# Returns: file contents or 404 if not found

POST /files/newfile.txt
# Creates/updates file with request body (201 Created)
```

**Root Path**
```bash
GET /
# Returns: empty 200 OK response
```

**Gzip Compression**
```bash
GET /echo/data HTTP/1.1
Accept-Encoding: gzip
# Response automatically compressed if client supports it
```

## Technical Stack

- **Language**: Python 3.14
- **Networking**: Python `socket` module
- **Concurrency**: Threading for multi-client handling
- **Compression**: Built-in `gzip` module

## Key Concepts Implemented

- **TCP Socket Programming** - Low-level socket operations and connection handling
- **HTTP Protocol Parsing** - Request/response line and header parsing
- **Threading & Concurrency** - Thread-per-client model for handling multiple connections
- **Content Encoding** - Dynamic compression negotiation with clients
- **File I/O** - Binary and text file handling with path validation
- **Error Handling** - Graceful handling of malformed requests and missing resources

## Getting Started

1. Clone the repository
2. Run `python app/main.py` to start the server
3. Test endpoints with `curl` or your HTTP client:
   ```bash
   curl http://localhost:4221/echo/test
   curl http://localhost:4221/user-agent
   curl -H "Accept-Encoding: gzip" http://localhost:4221/echo/data
   ```

## Future Enhancements

This project serves as a foundation for exploring advanced HTTP features:
- **HTTPS/TLS** - Secure socket layer implementation
- **WebSocket Support** - Real-time bidirectional communication
- **E-Tag Caching** - Efficient resource validation and caching
- **HTTP/2 Protocol** - Multiplexing and server push
- **Performance Optimization** - Async I/O with asyncio or uvloop

## Project Context

This implementation was completed as part of the CodeCrafters "Build Your Own HTTP Server" challenge, demonstrating proficiency in systems programming, network protocols, and low-level Python development.

---

*Built from scratch to understand how the web works at the protocol level.*
