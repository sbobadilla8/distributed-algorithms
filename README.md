# COMP90020 - Distributed algorithms

## Team
- Name: Roko's Basilisk
- Members:
  - Sebastian Bobadilla - 1305851
  - Suhrid Gupta - 1313675

## Topic
Mutual Exclusion

## Description of the app
For the application of the mutex we chose to implement a peer-to-peer file
sharing app. In this app all clients connect initially to an index server
that keeps track of the files and the clients that shared them. Then, 
after querying the server for a file and getting the list of clients and their
addresses, the file is transmitted in blocks through TCP connections.

## Algorithm implemented
The algorithm that we implemented for ensuring the file is not corrupted
is a mutex algorithm described in [Hemlock](https://dl.acm.org/doi/10.1145/3409964.3461805).

## Installation of dependencies
### Frontend
All React dependencies are managed through pnpm package manager. For installing
dependencies and running the frontend locally first run ```pnpm i``` and then ```pnpm dev```.
### Backend and server
Enable a virtual environment, and then in each of the 'client/backend' and 'server'
directories run ```pip3 install -r requirements.txt```.

## How to run the app
1. Run ```python3 idxServer.py``` found inside the 'server' directory.
2. Run ```python3 client.py``` found inside the 'client/backend' directory.

If any changes were made to the frontend, run ```pnpm build```, which will
export the build of the React app to the backend.