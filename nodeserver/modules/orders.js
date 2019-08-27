const uuidv4 = require('uuid/v4');
var balances = require('./balances.js');
var orders = []

function place_buylimit(market, quantity, rate, tisBuye){
    var uuid = uuidv4(); // ⇨ '1b9d6bcd-bbfd-4b2disBuydfbbd4bed'
    var now = new Date();
    orders.push({
        "OrderUuid": uuid,
        "Exchange": market,
        "OrderType": "buy",
        "PricePerUnit": rate,
        "Quantity": quantity,
        "Opened": now.toISOString(),
        "Closed": null
    })
    /*"result": [
    {
      "OrderUuid": "fd97d393-e9b9-4dd1-9dbf-f288fc72a185",
      "Exchange": "BTC-LTC",
      "TimeStamp": "string (date-time)",
      "OrderType": "string",
      "Limit": 1e-8,
      "Quantity": 667.03644955,
      "QuantityRemaining": 0,
      "Commission": 0.00004921,
      "Price": 0.01968424,
      "PricePerUnit": 0.0000295,
      "IsConditional": false,
      "Condition": "",
      "ConditionTarget": 0,
      "ImmediateOrCancel": false,
      "Closed": "2014-02-13T00:00:00"
    }
  ]*/
    return uuid;
}

function place_selllimit(market, quantity, rate, timeInForce){
    var uuid = uuidv4(); // ⇨ '1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed'
    var now = new Date();
    orders.push({
        "OrderUuid": uuid,
        "Exchange": market,
        "OrderType": "sell",
        "PricePerUnit": rate,
        "Quantity": quantity,
        "Opened": now.toISOString(),
        "Closed": null
    })
    return uuid;
}

function get_order(uuid){
    console.log(orders);
    console.log("UUID: " + uuid);
    for(var i = 0; i < orders.length; i++){
        if(orders[i]['OrderUuid'] == uuid){
            console.log("Found it!");
            return orders[i];
        }
    }
    return {};
}

function close_order(order){
    var now = new Date();
    if(order.Closed == null){
        order.Closed = now.toISOString();
        if(order.OrderType == "sell"){
            balances.sell(order.Exchange, order.Quantity)
        }
        else{
            balances.buy(order.Exchange, order.Quantity)
        }
    }
    else{
        console.log("Order already closed!");
    }
    return order;
}

function update(){
    for(var i = 0; i < orders.length; i++){
        orders[i] = close_order(orders[i]);
    }
}

module.exports = {
    "place_buylimit": place_buylimit,
    "place_selllimit": place_selllimit,
    "get_order": get_order,
    "update": update
}