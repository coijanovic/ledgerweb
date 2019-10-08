# What is ledgerweb?

Ledgerweb is intended to be run as a local webservice. It provides an easy way to add entries to a [ledger](https://ledger-cli.org)-file.

# Dependencies

- `python3`
    - `flask`
    - `subprocess`
- `rclone`

# Install 

1. Clone this repository
2. Setup your cloud storage with `rclone config` and edit line 45 in `ledgerweb.py` to match your configuration
    - to only use local storage, remove line 45 from `ledgerweb.py`
3. `python3 ledgerweb.py`
