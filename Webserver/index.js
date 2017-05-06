var mysql = require('mysql');
var express = require('express');

var dbConnection = mysql.createConnection({
    host: 'localhost',
    user: 'test',
    password: 'test',
    database: 'ttc_bus_data'
});

var app = express();

dbConnection.connect(function(err){
    if(!err) {
        console.log('Connected to database successfully')
    } else {
        console.log('Error: Could not connect to database')
    }
});

app.get("/", function(req, res){
    dbConnection.query('SELECT * from vehicle_locations',
    function(err, rows, fields) {
        dbConnection.end();
        if(!err) {
            res.send(rows)
        } else {
            console.log('Error: MySQL Query Failed')
        }
    })
});

app.listen(3000);