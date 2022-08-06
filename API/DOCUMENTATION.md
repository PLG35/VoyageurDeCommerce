# VoyageurDeCommerce API
API to use the VoyageurDeCommerce tool through http requests.

## User guide

### End points

#### /optimize
This endpoint returns the optimized path through the towns which coordinates are given through parameters.

The URL shall be as follow : http://{{server}}:{{port}}/api/v1.0/optimize.

The coordinates of the towns shall be given in x-www-form-urlencoded format with the key "villes".

### Examples
Examples of calls to the API can be found in the postman collection under API/tst.

In the collection variables, server is where the node server has been launched.
The port is the port of the server listening the calls. It is defined in the config.json under API/src.