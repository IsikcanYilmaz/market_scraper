var express = require('express');
var router = express.Router();

const better_sqlite3 = require('better-sqlite3');

const app = express();

const TL_SYMBOL = "₺";

const DATABASE_FILE = "./products.db";
var dbConnection = new better_sqlite3(DATABASE_FILE, {verbose: console.log});

app.use('/scripts', express.static(__dirname + '/scripts/'));

let prepStr = "";

function getListOfMarkets()
{
	var query = "SELECT DISTINCT market FROM products";
	var statement = dbConnection.prepare(query);
	var markets = statement.all();
	var retArr = [];
	for (i in markets)
	{
		retArr.push(markets[i].market);
	}
	return retArr;
}

function getListOfAvailDates()
{
	var query = "SELECT DISTINCT date, timestamp FROM products ORDER BY timestamp DESC";
	var statement = dbConnection.prepare(query);
	var dates = statement.all();
	var retArr = [];
	for (i in dates)
	{
		retArr.push(dates[i].date);
	}
	return retArr;
}

function getListOfCategories(market)
{
	var query = `SELECT DISTINCT category FROM products WHERE (market = '` + market + `')`;
	var statement = dbConnection.prepare(query);
	var categories = statement.all();
	var retArr = [];
	for (i in categories)
	{
		retArr.push(categories[i].category);
	}
	return retArr;
}

function getMarketDataByDate(market, category, date)
{
	var query = "";
	if (category == "*")
	{
		query = `SELECT DISTINCT name, currentPrice, oldPrice FROM products WHERE (date = '` + date + `') and (market = '` + market + `') ORDER BY category`;
	}
	else
	{
		query = `SELECT DISTINCT name, currentPrice, oldPrice FROM products WHERE (date = '` + date + `') and (market = '` + market + `') and (category = '` + category + `') ORDER BY category`;
	}
	console.log(query);
	var statement = dbConnection.prepare(query);
	var products = statement.all();
	console.log(products);
	var prepStr = ""
	for (i in products)
	{
		var product = products[i];
		var label1 = {content: product.name + " " + product.currentPrice + " " + TL_SYMBOL, xOffset:0, yOffset:0};
		var productPrepStr = ""
		if (product.oldPrice != "None")
		{
			productPrepStr += (`{group:2, x:\"` + i + `\", y: ` + product.currentPrice + `},`);
			productPrepStr += (`{group:1, x:\"` + i + `\", y: `+ product.oldPrice + `, label: ` + JSON.stringify(label1) + `},`);
		}
		else
		{
			productPrepStr += (`{group:2, x:\"` + i + `\", y: ` + product.currentPrice + `, label: `+ JSON.stringify(label1) + `},`);
		}
		prepStr += productPrepStr;
	}
	return prepStr;
}

function prepRenderData()
{
}

/* INIT PREP */
var markets = getListOfMarkets();
var marketsHtml = "";
for (i in markets)
{
	marketsHtml += ` <option id="market_` + markets[i] + `">` + markets[i] + `</option>`;
}

var dates = getListOfAvailDates();
var datesHtml = "";
for (i in dates)
{
	datesHtml += ` <option id="date_` + dates[i] + `">` + dates[i] + `</option>`;
}

var categories = getListOfCategories(markets[0]);
var categoriesHtml = "";
for (i in categories)
{
	console.log(categories[i]);
	categoriesHtml += ` <option id="category_` + categories[i] + `">` + categories[i] + `</option>`;
}
// console.log(categoriesHtml);

var etctext = "TEST"

/* GET home page. */
router.get('/', function(req, res, next) {
	console.log("HOME");
	res.render("index.ejs", {"title":"CAKMA CIMRI", 
		"markets":marketsHtml, 
		"categories":categoriesHtml, 
		"dates":datesHtml, 
		"etctext":"TEST"});
});

/* TODO GRAPH PAGE */
router.get('/graph', function(req, res, next) {
	console.log("GRAPH", req.query);
	var date = req.query.date;
	var market = req.query.market;
	var category = req.query.category;
	var jsonStr = getMarketDataByDate(market, category, date);
	res.render("graph.ejs", {"items":jsonStr, 
		"market":market, 
		"date":date, 
		"markets":marketsHtml, 
		"categories":categoriesHtml, 
		"dates":datesHtml, 
		"title":"CAKMA CIMRI"});
});

module.exports = router;
// module.exports = app;
