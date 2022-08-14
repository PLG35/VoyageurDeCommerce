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

function isVillesValid(str, configLimitNumberOfVilles){
    output = true;

    // Test the list of coordinates is between square brackets
    if(str[0] == "[" && str[str.length-1] == "]"){
        str = str.substring(1, str.length - 1);
        arr = str.split("],[");

        // Test the number of coordinates is between 1 and configLimitNumberOfVilles provided in the config.json
        if(arr.length > 0 && arr.length < configLimitNumberOfVilles){
            var test = 0;

            // Test each coordinate has the right format
            arr.forEach(function(element){
                element = element.replace('[', '');
                element = element.replace(']', '');

                arr2 = element.split(",");
                if(arr2.length != 2){
                    console.log("Town coordinates should contain two values : " + String(arr2) + " in " + element);
                    test++;
                }
                else{
                    // Test each coordinate is made of two numbers
                    coordinate1 = parseFloat(arr2[0]);
                    coordinate2 = parseFloat(arr2[1]);

                    if(isNaN(coordinate1) || isNaN(coordinate2)){
                        console.log("Coordinates should be float numbers : " + coordinate1 + " or " + coordinate2 + " in " + element);
                        test++;
                    }
                }
            });

            if(test > 0){
                output = false;
            }
        }
        else{
            console.log("Number of towns should be between 1 and " + configLimitNumberOfVilles + " : " + String(arr));
            output = false;
        }
    }
    else{
        console.log("Request parameter should be between squared brackets : " + str[0] + str[str.length-1]);
        output = false;
    }

    return output;
}

function writeInLog(str, logPath){
    fs.appendFile(logPath, str, function(err){
        console.log(err);
    })
}

function answerRequest(req, res, pageErrorCode, message, configLogPath){
    // Log request and response in the logs
    var logMessage = '{"request":{"headers":' + JSON.stringify(req.headers) + ',"body":' + JSON.stringify(req.body) + '}, "response":' + message + '},\n';
    writeInLog(logMessage, configLogPath);

    // Send response
    res.writeHead(pageErrorCode, {"Content-Type" : "application/json"});
    res.write(message);
    res.end();
}

// Read configuration file
var pathConfig = "config.json";
fs.readFile(pathConfig, "utf8", function(error, data){
    // Debug
    assert.equal(error, null);

    // Create variables from configuration file
    var configJSON = JSON.parse(data);
    var configApiVersion = configJSON.apiVersion;
    var configApiPort = configJSON.apiPort;
    var configLimitNumberOfVilles = configJSON.limitNumberOfVilles;
    var configLogPath = configJSON.logPath;

    // Generic entry point
    app.post('/' + configApiVersion + '/:page', function(req, res){
        // Case of the endpoint : optimization
        if(req.params.page == "optimize"){
            // console.log(req.body);

            // Test the validity of the request
            if(req.body.hasOwnProperty("villes")){

                // Get data from request
                var villes = req.body.villes;

                // Make sure the input has the format expected
                if(isVillesValid(villes, configLimitNumberOfVilles)){
                    var commande = "python apiVoyageur.py " + villes;
                    console.log(commande);

                    // Launch optimization script
                    exec(commande, function(error, stdout, stderr){
                        assert.strictEqual(error, null);
                        console.log(stderr);
                        console.log(stdout);

                        // Send server response when error
                        if(stderr != ""){
                            var pageErrorCode = 500;
                            var errorMessage = '{"errorID":"1000", "message":"The URL you are using is valid. And it does contain the right parameters, with data in the right format. However, the API server faced an issue providing a valid response to your request."}';
                            answerRequest(req, res, pageErrorCode, errorMessage, configLogPath);
                        }

                        // Send server response when everything is OK
                        else{
                            var pageErrorCode = 200;
                            answerRequest(req, res, pageErrorCode, stdout, configLogPath);
                        }
                    });
                }
                
                else{
                    // Error code for this case according to : https://restfulapi.net/http-status-codes/
                    var pageErrorCode = 400
                    var errorMessage = '{"errorID":"0020", "message":"The URL you are using is valid. And it contains the right parameters. However, the format of the value of the parameters is not valid. Please check in the documentation which data is required by this request."}';
                    answerRequest(req, res, pageErrorCode, errorMessage, configLogPath);
                }
            }
            
            else{
                // Error code for this case according to : https://restfulapi.net/http-status-codes/
                var pageErrorCode = 400
                var errorMessage = '{"errorID":"0010", "message":"The URL you are using is valid. However, it does not contain the required parameters. Please check in the documentation which data is required by this request."}';
                answerRequest(req, res, pageErrorCode, errorMessage, configLogPath);
            }
        }

        // Invalid URL for the request
        else{
            // Error code for this case according to : https://restfulapi.net/http-status-codes/
            pageErrorCode = 400
            var errorMessage = '{"errorID":"0002", "message":"The URL you are using is invalid. Please check the valid URL in the documentation."}';
            answerRequest(req, res, pageErrorCode, errorMessage, configLogPath);
        }
    });

    // Default answer for a call on the right port but with uncatched url / http method
    app.all('*', function(req, res){
        // Error code for this case according to : https://restfulapi.net/http-status-codes/
        pageErrorCode = 400
        var errorMessage = '{"errorID":"0001", "message":"The URL or HTTP method you are using is invalid. Please check the valid URL and HTTP method in the documentation."}';
        answerRequest(req, res, pageErrorCode, errorMessage, configLogPath);
    });

    // Listen the API port
    app.listen(configApiPort);
});