# Modbus TCP Viewer

A simple Flask-based web app that connects to a Modbus TCP server (running locally via `pymodbus`), reads Coils, Discrete Inputs, Holding Registers, and Input Registers, and displays them in a web UI.

---

## Features

- Modbus TCP client using `pyModbusTCP`
- Embedded Modbus TCP server using `pymodbus`
- Flask REST API and frontend
- Docker support for deployment
- GitHub Actions CI/CD pipeline with testing

---

## Run with Docker

Build and run the container:

```bash
docker build -t modbus-app .
docker run -p 5000:5000 -p 1502:1502 modbus-app
````

Or using Docker Compose:

```bash
docker-compose up
```

Visit: [http://localhost:5000](http://localhost:5000)

---

## Run Tests

Locally:

```bash
pytest test_modbus.py
```

Inside Docker container:

```bash
docker exec modbus-test pytest test_modbus.py
```

Tests are also automatically executed on push using GitHub Actions.

---

## Requirements

* Python 3.12+
* Flask
* pyModbusTCP
* pymodbus==2.5.3
* pytest

Install locally:

```bash
pip install -r requirements.txt
```

---
