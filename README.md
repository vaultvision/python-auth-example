# Python Auth Example

Sample application with authentication using OpenID Connect written in Python.


## Quick Start

Install dependencies (with make):
```bash
make
```

Install dependencies (manually):
```bash
python -m venv .venv  # Or python3 for some systems
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```


Configure app [.env](.env.defaults) file:
```
cp .env.defaults .env
vi .env  # Set your VV_ISSUER_URL
```


Run the example on localhost (with make):
```bash
make run
```

Run the example on localhost (manually):
```bash
.venv/bin/python app.py
```


Visit [http://localhost:8090](http://localhost:8090) in your browser.


## Who are we?

[Vault Vision](https://docs.vaultvision.com) is built on open source technologies and is committed to building a welcoming community developers can trust.

Visit [https://docs.vaultvision.com](https://docs.vaultvision.com) to learn more!


----

Vault Vision projects adopt the [Contributor Covenant Code of Conduct](https://github.com/vaultvision/.github/blob/main/CODE_OF_CONDUCT.md) and practice responsible disclosure as outlined in our [Security Policy](https://github.com/vaultvision/.github/blob/main/SECURITY.md).
