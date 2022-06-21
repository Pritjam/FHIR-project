const querystring = require('querystring')
var http = require('http');
const fs = require('fs');
const url = require('url');
const request = require('request');

http.createServer(function (req, res) {

    var q = url.parse(req.url, true);
    if (q.pathname == '/getpatientdata') {
        getPatientData(req, res);
    } else {
        res.writeHead(200, { 'content-type': 'text/html' });
        fs.createReadStream('index.html').pipe(res);
    }

}).listen(8080);

function getPatientData(req, res) {
    res.writeHead(200, { 'Content-Type': 'text/html' });

    let rawData = ''
    req.on('data', chunk => {
        rawData += chunk
    })
    
    req.on('end', () => {
        let parsedData = querystring.decode(rawData)
        var patientid = parsedData.patientid;
        res.write("Patient ID: " + patientid + "<br>");
        let baseURL = "https://server.fire.ly/"
        let operation = "Patient/"

        request.get({
            url: baseURL + operation + patientid,
            json: true,
            headers: { 'Accept': 'application/fhir+json' }
        }, function (err, resp, body) {
            if (err) { return console.log(err); }
            res.write(body.text.div);
            // console.log(body);
            res.end();
        })
    })
}
