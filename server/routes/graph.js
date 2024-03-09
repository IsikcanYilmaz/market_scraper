var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
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
