# What is ledgerweb?

[ledger-cli](https://ledger-cli.org) is great. It offers a powerful double-entry accounting system with all data in a plain text file.
But its reliance on the command line make it not very accessible for "normal" people. This is where ledgerweb comes in: It provides an easy to use web-interface for adding entries to your ledger-file and viewing commonly used reports.

# What is the intended use-case for ledgerweb?

ledger-web is intended to be run as a local website (only accessible from within your home network) on a Raspberry Pi or something similar.
The data is automatically synced to a cloud storage provider of your choice using [rclone](https://rclone.org). 

# Requirements

1. A device to run the service (anything from a Raspberry Pi Zero W and up should work)
2. Access to cloud storage compatible with rclone (see [rclone.org](https://rclone.org) for a full list). Note: you can also encrypt any supported cloud storage with rclone, which might be a good idea with sensible financial information.

If you don't want to use rclone, you can change lines 18 and 19 (`sync_down` and `sync_up`) in `ledgerweb.py` to something that suits your needs (e.g. `rsync` if you want to sync your ledger data across your local network)

# Install

1. Setup `python3` with the following packages:
    - `flask`
    - `subprocess`
    - `pyyaml`
2. Install `rclone` and setup your cloud storage
3. Install `ledger`
4. Clone this repository
5. Customize your ledgerweb-instance by creating your own `config.yaml` file in the ledgerweb folder (see ch. config)
6. Run the server with `python3 /path/to/ledgerweb/ledgerweb.py`

# Config

The configuration of ledgerweb is done in a [yaml](https://yaml.org) file. 
Please create the file `config.yaml` for your own configuration. See `defaultconfig.yaml` for all available options and syntax.

Note: The config-file is only parsed on startup. If you change your configuration, you have to stop flask (`Ctrl-C`) and start it again for your changes to be effective.j


| Key        | Explanation                                                                                    |
|------------|------------------------------------------------------------------------------------------------|
| hostip     | ip address used by flask, should be the ip of your server                                      |
| hostport   | port used by flask, use 80 for (local) deployment                                              |
| remotename | name of the rclone remote to which you want to sync your ledger data                           |
| remotepath | directory on remote to which you want to sync your ledger data                                 |
| currency   | currency used in ledger file                                                                   |
| accounts   | a list of commonly used accounts (e.g. `Assets:Checking`) to be used as data for auto-complete |
| favs       | often used transactions, with `from` and `to`-account
