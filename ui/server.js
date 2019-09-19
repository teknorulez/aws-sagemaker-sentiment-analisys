const express = require('express');
const path = require('path');
const port = process.env.PORT || 8080;
const app = express();

var fs = require('fs');

app.use('/img', express.static(__dirname + '/img'));
app.use('/scripts', express.static(__dirname + '/scripts'));

// serve static assets normally
app.get('*.css', function css(request, response) {
  if (request.url.indexOf(".css") !== -1){
    var file = fs.readFileSync(`.${request.url}`, {'encoding' : 'utf8'});
    response.writeHead(200, {'Content-Type' : 'text/css'});
    response.write(file);
    response.end();
  }
});

// handle every other route with index.html, which will contain
// a script tag to your application's JavaScript file(s).
app.get('*', function (request, response) {
  response.sendFile(path.resolve(__dirname, 'index.html'));
});

app.listen(port);
console.log("server started on port " + port);