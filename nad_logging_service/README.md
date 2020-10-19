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

- [ ] Format log entries
- [ ] Adjust transports to allow multiple logger services running.
- [ ] Implement log schema
- [ ] Separate loggers for API and app.
- [ ] Add master key to dotenv
- [ ] Implement processName, Id
- [ ] Implement manual testing in client

- [ ] CLEANUP: remove app registration route.
- [ ] Remove db and registry module
