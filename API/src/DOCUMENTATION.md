# VoyageurDeCommerce API
API to use the VoyageurDeCommerce tool through http requests.

## Developer guide

### Dependencies
The code is made to run on Python 3.

The library libVoyageur.py is a copy of the file at the root folder of the project.

The apiVoyageur.py is the bridge between the http server receiving the calls and the library libVoyageur.py. It has the following dependencies to python libraries :
 - libVoyageur
 - sys
 - time
 - copy
 - json

The http server server.js is written in node. It shall be started on a machine before it can be called. It has the following dependencies to node libraries :
 - fs
 - assert
 - express
 - child_process
 - body-parser

The http server server.js find configuration information from the file config.json. In particular, it contains the version of the api and the port on which the server shall listen for calls.