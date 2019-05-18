const bodyParser = require("body-parser");
const express = require("express");
const request = require("request");
const exec = require('child_process').exec;

var app = express();
var port = process.env.PORT || process.env.port || 5000;
app.set("port", port);

app.use(bodyParser.json());
app.listen(app.get("port"), function () {
    console.log("[app.listen]Node app is running on port", app.get("port"));
});
module.exports = app;

app.post("/webhook", function (req, res) {
    let data = req.body;
    let donkeygo01 = data.queryResult.parameters.any;
    let donkeygo = donkeygo01.toUpperCase()
    if (donkeygo == "A"){
        let command_str = 'python3 ~/cust_func/A_line_client.py A'
        exec(command_str, (error,stdout, stderr) => {
            console.log(stdout);
        })
        console.log('go to A port')
    }
    else if (donkeygo == "B"){
        let command_str = 'python3 ~/cust_func/A_line_client.py B'
        exec(command_str, (error,stdout, stderr) => {
            console.log(stdout);
        })
        console.log('go to B port')
    }
    else if (donkeygo == "C"){
        let command_str = 'python3 ~/cust_func/A_line_client.py C'
        exec(command_str, (error,stdout, stderr) => {
            console.log(stdout);
        })
        console.log('go to C port')
    }
    else{
	console.log(donkeygo)
        return console.log('error')
    }
});
