# http-server-python

An HTTP/1.1 compliant web server built from scratch in Python using raw socket programming — no frameworks, no external libraries. Implements a meaningful subset of RFC 2616.

![Python](https://img.shields.io/badge/Python-3.11-blue) ![Sockets](https://img.shields.io/badge/Networking-Sockets-orange) ![Threading](https://img.shields.io/badge/Concurrency-Threading-yellow)

---

## Why This Exists

Most web developers use frameworks without understanding the protocol underneath. This project was built to understand exactly what happens between a browser sending a request and receiving a response — at the TCP socket level.

---

## What It Implements

- **HTTP/1.1 protocol** — proper request line parsing, header handling, status codes
- **Concurrent connections** — multi-threaded architecture handles multiple clients simultaneously
- **GET and POST methods** — with correct request body parsing and response building
- **Static file serving** — reads and serves files from a configurable directory
- **File uploads** — handles multipart POST request bodies
- **Gzip compression** — reads `Accept-Encoding` header and compresses responses when supported
- **Persistent connections** — supports `Connection: keep-alive`

---

## Quick Start

```bash
git clone https://github.com/arsham909/http-server-python.git
cd http-server-python
python server.py
```

Test it:
```bash
# Basic GET request
curl -v http://localhost:4221/

# Test gzip encoding
curl -v --compressed http://localhost:4221/

# POST request
curl -v -X POST http://localhost:4221/upload -d "hello=world"
```

---

## Architecture

```
TCP Socket (bind → listen → accept)
         │
         ▼
Thread spawned per connection
         │
         ▼
Request Parser
  ├── Request line (method, path, version)
  ├── Headers (key-value pairs)
  └── Body (for POST)
         │
         ▼
Router (path → handler)
         │
         ▼
Response Builder
  ├── Status line
  ├── Headers (Content-Type, Content-Encoding, etc.)
  └── Body (with optional gzip compression)
```

---

## What This Demonstrates

- TCP/IP socket programming in Python
- RFC 2616 HTTP/1.1 protocol compliance
- Thread-safe concurrent server design
- Manual HTTP request and response parsing
- Content negotiation (gzip compression)
- Low-level understanding of how web frameworks work internally
