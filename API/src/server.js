// Requires
const fs = require('fs');
const assert = require('assert');

// Express
const express = require('express');
const { exec } = require('child_process');
const { json } = require('body-parser');
const app = express();
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

// Read configuration file
var pathConfig = "config.json";
fs.readFile(pathConfig, "utf8", function(error, data){
    // Debug
    assert.equal(error, null);

    // Create variables from configuration file
    var configJSON = JSON.parse(data);
    var configApiVersion = configJSON.apiVersion;
    var configApiPort = configJSON.apiPort;

    // Generic entry point
    app.post('/' + configApiVersion + '/:page', function(req, res){
        // Case of optimization endpoint
        if(req.params.page == "optimize"){
            // console.log(req.body);

            // Test the validity of the request
            if(req.body.hasOwnProperty("villes")){

                // Get data from request
                var villes = req.body.villes;
                var commande = "python apiVoyageur.py " + villes;
                console.log(commande);

                // Launch optimization script
                exec(commande, function(error, stdout, stderr){
                    assert.strictEqual(error, null);
                    console.log(stderr);
                    console.log(stdout);

                    // Send server response when error
                    if(stderr != ""){
                        pageErrorCode = 500;

                        // Provide error message
                        var errorMessage = '{"message":"The URL you are using is valid. And it does contain the required data. However, the API server faced an issue providing a valid response to your request."}';

                        res.writeHead(pageErrorCode, {"Content-Type" : "application/json"});
                        res.write(errorMessage);
                        res.end();
                    }

                    // Send server response when everything is OK
                    else{
                        pageErrorCode = 200;
                        res.writeHead(pageErrorCode, {"Content-Type" : "application/json"});
                        res.write(stdout);
                        res.end();
                    }
                });
            }
            
            else{
                // Error code for this case according to : https://restfulapi.net/http-status-codes/
                pageErrorCode = 400
                
                // Provide error message
                var errorMessage = '{"message":"The URL you are using is valid. However, it does not contain the required data. Please check in the documentation which data is required by this request."}';

                // Send server response
                res.writeHead(pageErrorCode, {"Content-Type" : "application/json"});
                res.write(errorMessage);
                res.end();
            }
        }

        // Invalid URL for the request
        else{
            // Errorcode for this case according to : https://restfulapi.net/http-status-codes/
            pageErrorCode = 400

            // Provide error message
            var errorMessage = '{"message":"The URL you are using is invalid. Please check the valid URL in the documentation."}';

            // Send server response
            res.writeHead(pageErrorCode, {"Content-Type" : "application/json"});
            res.write(errorMessage);
            res.end();
        }
    });

    // Listen the API port
    // TODO : test that if another port is used a 404 error is returned
    app.listen(configApiPort);
});