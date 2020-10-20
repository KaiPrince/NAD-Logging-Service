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
- [ ] Separate loggers for API and app.
- [ ] Add master key to dotenv
- [ ] Implement manual testing in client

- [ ] CLEANUP: remove app registration route.
- [ ] Remove db and registry module
- [ ] overwrite datetime if provided.
