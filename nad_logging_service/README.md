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
- [x] Store two datetime (one client, one server)
- [x] Standardize datetime to ISO
- [x] rate limit routes (1 per second on all routes)
- [x] write exception tests
- [x] malformed logs & error checking
- [ ] stack tracing
- [ ] json web tokens (optional)
- [x] limit log request size
- [ ] move config to json file
- [ ] move client datetime format to config file.
- [x] verify datetime from client
- [x] log when rate limit is hit
- [x] send error code instead of crashing

- [x] CLEANUP: remove app registration route.
- [x] Separate loggers for API and app.
- [x] Remove db and registry module
- [ ] Add catch all error route
- [x] Add validation
- [ ] encrypt messages & data
