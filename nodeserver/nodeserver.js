console.log("Testing!");
const express = require('express');
var cors = require('cors');
var order = require('./modules/buySell');
var common = require('./modules/currentStats');
var multer  = require('multer');
var bodyParser = require('body-parser');
const path = require('path');
var compression = require('compression')
var constants = require('./modules/constants');
const app = express();
let shouldStop = false;
//Middleware
// use it before all route definitions
app.use(cors({origin: ['http://localhost:4200']}));
//Allow usage of json format.
app.use(express.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use(compression());
var server = require('http').createServer(app);

const storage = multer.diskStorage({
    destination: function(req, file, cb) {
        cb(null, './latestData/');
    },
    filename: function(req, file, cb) {
        cb(null, file.originalname);
    }
});

let upload = multer({storage: storage});

//Static directories
app.use("/latestData", express.static(__dirname + '/latestData'));


app.get('/market/buylimit', (req,res)=>{
    var market = req.query.market;
    var quantity = req.query.quantity;
    var rate = req.query.rate;
    var timeInForce = req.query.timeInForce;
    /*{
  "success": true,
  "message": "''",
  "result": {
    "uuid": "614c34e4-8d71-11e3-94b5-425861b86ab6"
  }
}*/
});

app.get('/market/selllimit', (req,res)=>{
    var market = req.query.market;
    var quantity = req.query.quantity;
    var rate = req.query.rate;
    var timeInForce = req.query.timeInForce;
    /*{
  "success": true,
  "message": "''",
  "result": {
    "uuid": "614c34e4-8d71-11e3-94b5-425861b86ab6"
  }
}*/
});

app.get('/market/getopenorders', (req,res)=>{
    var market = req.query.market;
    /*{
  "success": true,
  "message": "''",
  "result": [
    {
      "Uuid": "string (uuid)",
      "OrderUuid": "8925d746-bc9f-4684-b1aa-e507467aaa99",
      "Exchange": "BTC-LTC",
      "OrderType": "string",
      "Quantity": 100000,
      "QuantityRemaining": 100000,
      "Limit": 1e-8,
      "CommissionPaid": 0,
      "Price": 0,
      "PricePerUnit": null,
      "Opened": "2014-07-09T03:55:48.583",
      "Closed": null,
      "CancelInitiated": "boolean",
      "ImmediateOrCancel": "boolean",
      "IsConditional": "boolean"
    }
  ]
}*/
});

app.get('/account/getbalances', (req,res)=>{
    /*{
  "success": true,
  "message": "''",
  "result": [
    {
      "Currency": "DOGE",
      "Balance": 4.21549076,
      "Available": 4.21549076,
      "Pending": 0,
      "CryptoAddress": "DLxcEt3AatMyr2NTatzjsfHNoB9NT62HiF",
      "Requested": false,
      "Uuid": null
    }
  ]
}*/
});

app.get('/account/getbalance', (req,res)=>{
    var currencty = req.query.currency;
    /*{
  "success": true,
  "message": "''",
  "result": {
    "Currency": "DOGE",
    "Balance": 4.21549076,
    "Available": 4.21549076,
    "Pending": 0,
    "CryptoAddress": "DLxcEt3AatMyr2NTatzjsfHNoB9NT62HiF",
    "Requested": false,
    "Uuid": null
  }
}*/
});


app.get('/ping', (req,res)=>{
    console.log("Good job, you pinged the server.");
});

server.listen(8080, () => console.log('Proxy app listening on port ' + constants.port + '!'));