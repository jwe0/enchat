# Enchat
> Enchat is an e2ee messaging app

## Features
> - Self hosted servers
> - RSA cryptography
> - E2EE

## Setup
1. For the first step you will require a supabse account. Place your supabse url and api key in the .env.example and remove the .example from the end.
2. Run `pip install -r requirements.txt` to install requirements
3. Run `python3 server.py` to run the server
4. Run `python3 client.py` to start a client
5. In the client execute `set HOSTNAME PORT` to set your server
6. Then run `register USERNAME PASSWORD` to register an account with the server you specified
7. You can now send messages to other people by executing `send TARGET_USERNAME MESSAGE`

## Issues
Any issues please open a GitHub issue and if you would like to contribute open a PR