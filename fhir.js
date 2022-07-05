const querystring = require('querystring')
var http = require('http');
const fs = require('fs');
const url = require('url');
const request = require('request');

http.createServer(function (req, res) {

    var parsedURL = url.parse(req.url, true);
    if (parsedURL.pathname == '/getpatientdata') {
        getPatientData(req, res, parsedURL);
    } else {
        res.writeHead(200, { 'content-type': 'text/html' });
        fs.createReadStream('new_index.html').pipe(res);
    }

}).listen(8080);

function getPatientData(req, res, parsedURL) {
    res.writeHead(200, { 'Content-Type': 'text/html' });

    var patientid = parsedURL.query.patientid;
    res.write("Patient ID: " + patientid + "<br>");
    let baseURL = "https://server.fire.ly/"
    let operation = "Patient/"

    request.get({
        url: baseURL + operation + patientid,
        json: true,
        headers: {  'Accept': 'application/fhir+json',
                    'Access-Control-Allow-Origin': '*'}
    }, function (err, resp, body) {
        if (err) { return console.log(err); }
        if(body == null || body.text == null) {
            res.write("Error: invalid response recieved");
            res.end();
            return console.log("Error: invalid response recieved");
        }
        res.write(JSON.stringify(body, null, 2));
        res.end();
    })
}
