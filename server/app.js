const express = require('express') //import express
const bodyParser = require('body-parser') //import body parser to work with express
require('dotenv').config(); //import dotenv so that it can read .env files

const PORT = process.env.PORT || 3000; //set the port from the env variable, if there is no port defined then fallback to 3000

const app = express() //set express to variable app
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(express.static(__dirname + "/../client/")); //Setting the file path to serve static pages from client folder


app.use(function (req, res) { //incase there is no route, this will send an error 404 page not found
    res.send("<h1>ERROR 404<h1> <h2>Page not found</h2>");
});

app.listen(PORT, function(){  //must be placed last to listen to the port
    console.log('App running on port: '+PORT)
});