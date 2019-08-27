var request = require("request");
var fs = require('fs');
const path = require("path");
function separateTradeString(tradeString){
    var first_currency = "";
    var second_currency = "";
    var is_on_first = true;
    for (var i = 0; i < tradeString.length; i++){
        var x = tradeString[i];
        if(x === '-'){
            is_on_first = false;
            continue
        }
        if(is_on_first){
            first_currency = first_currency + x;
        }
        else{
            second_currency = second_currency + x;
        }
    }
    return {"first": first_currency, "second": second_currency};
}


function get_market_summary(tradeString, callback = (result)=>{}){
    request("https://api.bittrex.com/api/v1.1/public/getmarketsummary?market=" + tradeString, function(error, response, body) {
        console.log(body);
        console.log(JSON.parse(body).result);
        callback(JSON.parse(body).result);
    });
}


function get_wallet(callback = (result)=>{}){
    fs.readFile(path.resolve(__dirname, '../data/balances.json'), 'utf8', (err, jsonString) => {
        if (err) {
            console.log("Error reading file from disk:", err)
            return
        }
        try {
            var result = JSON.parse(jsonString);
            callback(result);
    } catch(err) {
            console.log('Error parsing JSON string:', err)
        }
    })
}

function update_wallet(wallet){
    fs.writeFile(path.resolve(__dirname, "../data/balances.json"), wallet, 'utf8', function (err) {
        if (err) {
            console.log("An error occured while writing JSON Object to File.");
            return console.log(err);
        }
        console.log("JSON file has been saved.");
    });
}

function buy(trade_string, how_much_spent, askPrice){
    console.log(trade_string);
    //Separating currencies into two different strings
    var data = separateTradeString(trade_string);
    console.log(data);
    var c_one = data['first'];
    var c_two = data['second'];

    //Getting the wallet
    get_wallet((wallet)=>{
         //Best price you can get for the trade
        var ask_price = askPrice;

        //Calculating how much to subtract and add from wallet
        how_much_spent = how_much_spent;
        var how_much_gained = how_much_spent / ask_price;

        console.log(how_much_spent);
        console.log(how_much_gained);
        console.log(c_one);
        console.log(c_two);
        console.log(wallet);
        if(!wallet.hasOwnProperty(c_two)){            
            console.log("You don't have " + c_two + " in your wallet yet! Creating...");
            wallet[c_two] = {c_two: {
                "Currency": c_two,
                "Balance": 0,
                "Available": 0,
                "Pending": 0,
                "CryptoAddress": "DLxcEt3Aatefgefg2NTatzjsfHNoT62HiF",
                "Requested": false,
                "Uuid": null
            }};
        }
        if(!wallet.hasOwnProperty(c_one)){            
            console.log("You don't have " + c_one + " in your wallet yet! Creating...");
            wallet[c_one] = {c_one: {
                "Currency": c_one,
                "Balance": 0,
                "Available": 0,
                "Pending": 0,
                "CryptoAddress": "DLxcEt3Aatefgefg2NTatzjsfHNoT62HiF",
                "Requested": false,
                "Uuid": null
            }};
        }
        //Changing values in the wallet
        wallet[c_one]["Balance"] -= how_much_spent;  //BTC
        wallet[c_two]["Balance"] += how_much_gained;  //LTC
        wallet[c_one]["Available"] = wallet[c_one]["Balance"];
        wallet[c_two]["Available"] = wallet[c_two]["Balance"];

        //Updating the wallet
        update_wallet(JSON.stringify(wallet));
    });

   

}

function sell(trade_string, how_much_sold, bidPrice){

    //Separating currencies into two different strings
    var data = separateTradeString(trade_string);
    var c_one = data['first'];
    var c_two = data['second'];

    //Getting the wallet
    get_wallet((wallet)=>{
        //Best price you can get for the trade
        var bid_price = bidPrice;

        //Calculating how much to subtract and add from wallet
        how_much_sold = how_much_sold;
        var how_much_gained = how_much_sold / bid_price;

        console.log(how_much_sold);
        console.log(how_much_gained);
        
        if(!wallet.hasOwnProperty(c_two)){            
            console.log("You don't have " + c_two + " in your wallet yet! Creating...");
            wallet[c_two] = {c_two: {
                "Currency": c_two,
                "Balance": 0,
                "Available": 0,
                "Pending": 0,
                "CryptoAddress": "DLxcEt3Aatefgefg2NTatzjsfHNoT62HiF",
                "Requested": false,
                "Uuid": null
            }};
        }
        if(!wallet.hasOwnProperty(c_one)){            
            console.log("You don't have " + c_one + " in your wallet yet! Creating...");
            wallet[c_one] = {c_one: {
                "Currency": c_one,
                "Balance": 0,
                "Available": 0,
                "Pending": 0,
                "CryptoAddress": "DLxcEt3Aatefgefg2NTatzjsfHNoT62HiF",
                "Requested": false,
                "Uuid": null
            }};
        }

        //Changing values in the wallet
        wallet[c_one]["Balance"] -= how_much_sold;  //BTC
        wallet[c_two]["Balance"] += how_much_gained;  //LTC
        wallet[c_one]["Available"] = wallet[c_one]["Balance"];
        wallet[c_two]["Available"] = wallet[c_two]["Balance"];

        //Updating the wallet
        update_wallet(JSON.stringify(wallet));

    });

    

}

module.exports = {
    "buy": buy,
    "sell": sell,
    "get_wallet": get_wallet

}