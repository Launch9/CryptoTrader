var request = require("request");
var fs = require('fs');

function separateTradeString(tradeString){
    var first_currency = "";
    var second_currency = "";
    var is_on_first = true;
    for (x in tradeString){
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
    fs.readFile('../data/balances.json', 'utf8', (err, jsonString) => {
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
    fs.writeFile("../data/balances.json", wallet, 'utf8', function (err) {
        if (err) {
            console.log("An error occured while writing JSON Object to File.");
            return console.log(err);
        }
        console.log("JSON file has been saved.");
    });
}

function buy(trade_string, how_much_spent){

    //Separating currencies into two different strings
    var data = separateTradeString(trade_string);
    var c_one = data['first'];
    var c_two = data['second'];

    //Getting the wallet
    var wallet = get_wallet();

    var summary = get_market_summary(trade_string);

    //Best price you can get for the trade
    var ask_price = summary[0]['Ask'];

    //Calculating how much to subtract and add from wallet
    how_much_spent = how_much_spent;
    var how_much_gained = how_much_spent / ask_price;

    console.log(how_much_spent);
    console.log(how_much_gained);
    

    //Changing values in the wallet
    wallet[c_one] -= how_much_spent;  //BTC
    wallet[c_two] += how_much_gained;  //LTC

    //Updating the wallet
    update_wallet(JSON.stringify(wallet));

}

module.exports = {
    "buy": buy,
    "get_wallet": get_wallet

}