# NAD-Logging-Service

A Logging Microservice written in Flask.

Requires Python.

## Installation

Install dependencies.

```
pip install -r requirements.txt
```

## Running

Optional: Set development mode (_powershell_)

```
$env:FLASK_ENV="development"
```

Run Flask

```
flask run
```

## TODO

- [ ] Adjust transports to allow multiple logger services running.
- [x] Add master key to dotenv
- [ ] Implement manual testing in client
- [ ] Store two datetime (one client, one server)
- [ ] Standardize datetime to ISO
- [x] rate limit routes (1 per second on all routes)
- [ ] write exception tests
- [ ] encrypt messages & data
- [ ] malformed logs & error checking
- [ ] stack tracing
- [ ] json web tokens (optional)

- [ ] CLEANUP: remove app registration route.
- [ ] Separate loggers for API and app.
- [ ] Remove db and registry module
- [ ] Add catch all error route
