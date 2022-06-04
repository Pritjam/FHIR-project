const formidable = require('formidable');
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
    var form = new formidable.IncomingForm();
    form.parse(req, function (err, fields, files) {
        var patientid = fields.patientid;
        res.write("Patient ID: " + patientid + "<br>");
        request('http://test.fhir.org/r2/Patient/' + patientid, { json: true }, (err, resp, body) => {
            if (err) { return console.log(err); }
            res.write(body.text.div);
            res.end();
        });
    });
}