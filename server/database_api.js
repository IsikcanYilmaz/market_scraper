const better_sqlite3 = require('better-sqlite3');

const DATABASE_FILE = "./products.db";

var dbConnection = new better_sqlite3(DATABASE_FILE, {verbose: console.log});

function getlistofmarkets()
{
	var query = "select distinct market from products";
	var statement = dbconnection.prepare(query);
	var markets = statement.all();
	var retarr = [];
	for (i in markets)
	{
		retarr.push(markets[i].market);
	}
	return retarr;
}

function getlistofavaildates()
{
	var query = "select distinct date, timestamp from products order by timestamp desc";
	var statement = dbconnection.prepare(query);
	var dates = statement.all();
	var retarr = [];
	for (i in dates)
	{
		retarr.push(dates[i].date);
	}
	return retarr;
}

function getlistofcategories(market)
{
	var query = `select distinct category from products where (market = '` + market + `')`;
	var statement = dbconnection.prepare(query);
	var categories = statement.all();
	var retarr = [];
	for (i in categories)
	{
		retarr.push(categories[i].category);
	}
	return retarr;
}

function getmarketdatabydate(market, category, date)
{
	var query = "";
	if (category == "*")
	{
		query = `select * from products where (date = '` + date + `') and (market = '` + market + `') order by category`;
	}
	else
	{
		query = `select * from products where (date = '` + date + `') and (market = '` + market + `') and (category = '` + category + `') order by category`;
	}
	console.log(query);
	var statement = dbconnection.prepare(query);
	var products = statement.all();
	// console.log(products);
	var prepstr = ""
	for (i in products)
	{
		var product = products[i];
		var label1 = {content: product.name + " " + product.currentprice + " " + tl_symbol, xoffset:0, yoffset:0};
		var productprepstr = ""
		if (product.oldprice != "none")
		{
			productprepstr += (`{group:2, x:\"` + i + `\", y: ` + product.currentprice + `},`);
			productprepstr += (`{group:1, x:\"` + i + `\", y: `+ product.oldprice + `, label: ` + json.stringify(label1) + `},`);
		}
		else
		{
			productprepstr += (`{group:2, x:\"` + i + `\", y: ` + product.currentprice + `, label: `+ json.stringify(label1) + `},`);
		}
		prepstr += productprepstr;
	}
	return prepstr;
}

function preprenderdata()
{
}
