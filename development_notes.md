# Notes for developers

Tests should be run against installed package:

```sh
git clone git@github.com:MasterSergius/acachecontrol.git
cd acachecontrol
pip install .
```

Then run tests:
`pytest tests` or `python -m pytest tests`

Supported python versions: 3.6+ (Note that asyncio.run() introduced in 3.7)

### Before commit

Run `make lint` to check code style ("black" automatically formats code, run again to re-check).
Run `make install test` to run all tests.
