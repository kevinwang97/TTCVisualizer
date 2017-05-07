var mysql = require('mysql');
var express = require('express');
var cors = require('cors');

var dbConnection = mysql.createConnection({
    host: 'localhost',
    user: 'test',
    password: 'test',
    database: 'ttc_bus_data'
});

var app = express();
app.use(cors());

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
        if(!err) {
            res.send(rows)
        } else {
            console.log('Error: MySQL Query Failed')
        }
    })
});

app.listen(3000);

function exitHandler(options, err) {
    if (options.cleanup) {
        dbConnection.end();
    }
    if (err) console.log(err.stack);
    if (options.exit) {
        console.log("exiting");
        process.exit();
    }
}

process.on('SIGINT', exitHandler.bind(null, {cleanup: true, exit:true}));
process.on('uncaughtException', exitHandler.bind(null, {exit:true}));
process.on('exit', exitHandler.bind(null,{cleanup:true}));
