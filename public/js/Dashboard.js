// var d3 = require('./d3');
queue()
    .defer(d3.json, "/api/data")
    .await(makeGraphs);
// function makeGraphs(error, apiData){
// 	var dataSet = apiData;
// 	// console.log(dataSet);
// 	for(i=0; i<dataSet.length; i++){
// 		dataSet[i].Date = new Date(dataSet[i].Date);
// 		//console.log(dataSet[i].Date);
// 		//console.log(typeof(dataSet[i].Date));
// 	}
// 	console.log(i);

// 	var ndx = crossfilter(dataSet);
// 	var datePosted = ndx.dimension(function(d) { return d.Date; });
// 	var projectsByDate = datePosted.group();

//  // };
//  	console.log(projectsByDate);
// 	var all = ndx.groupAll();

// 	var minDate = datePosted.bottom(1)[0].Date;
// 	var maxDate = datePosted.top(1)[0].Date;
// 	console.log(minDate);
// 	console.log(maxDate);

// 	var dateChart = dc.lineChart("#date-chart");

// 	dateChart
// 		//.width(600)
// 		.height(220)
// 		.margins({top: 10, right: 50, bottom: 30, left: 50})
// 		.dimension(datePosted)
// 		.group(projectsByDate)
// 		.renderArea(true)
// 		.transitionDuration(500)
// 		.x(d3.time.scale().domain([minDate, maxDate]))
// 		.elasticY(true)
// 		.renderHorizontalGridLines(true)
//     	.renderVerticalGridLines(true)
// 		.xAxisLabel("Date")
// 		.yAxis().ticks(6);
// 	dc.renderAll();
// };
// <!DOCTYPE html> <html>
// <head>
// <meta charset="utf-8"> 
// <script src="d3.js"></script> 
// <script>
// function draw(data) {
// ￼￼￼￼2 | Chapter 1: Introduction
// ￼"use strict";
// // badass visualization code goes here }
// </script> </head>
// <body> <script>
// d3.json("data/some_data.json", draw); </script>
// </body> </html>

// d3 offical document 
// function makeGraphs(error, apiData){
// 	// console.log(apiData);
// 	var margin = 40, width = 700 - margin, height = 300 - margin;
// 	var svg = d3.select("#date-chart").append("svg");

// 	svg.attr("width", width+margin)
// 	.attr("width", height+margin) 
// 	var g = svg.append("g")
// 	.attr("class","chart");

// 	var circle = svg.selectAll("circle.times_square")
// 	.data(apiData) 
// 	.enter() 
// 	.append("circle");

// 	circle.attr("class", "times_square");

// 	var price_extent = d3.extent( 
// 		apiData, function(d){return d[1]}
// 		);
// 	console.log(price_extent);

// 	var price_scale = d3.scale.linear().domain(price_extent).range([height, margin]);

// 	circle.attr("cy", function(d){return price_scale(d[1]);});

// 	var time_extent = d3.extent( apiData, function(d){return d[0]} );
// 	var time_scale = d3.time.scale() .domain(time_extent) .range([margin, width]);
// 	console.log(time_extent);

// 	circle.attr("cx", function(d){return time_scale(d[0]);});
// 	circle.attr("r", 3);
// 	var time_axis = d3.svg.axis() .scale(time_scale);

// 	svg.append("g")
// 	.attr("class", "x axis")
// 	.attr("transform", "translate(0," + height + ")") .call(time_axis);
// 	};

// d3 stock market
function makeGraphs(error, data){

	for(var i =0; i < data.length; i ++)
	{
		data[i][0] = parseInt(data[i][0]);
		data[i][1] = parseFloat(data[i][1]);
	};
	var margin = {top: 30, right: 20, bottom: 100, left: 50},
    margin2  = {top: 210, right: 20, bottom: 20, left: 50},
    width    = 764 - margin.left - margin.right,
    height   = 283 - margin.top - margin.bottom,
    height2  = 283 - margin2.top - margin2.bottom;

  	var parseDate = d3.time.format('%d/%m/%Y').parse,
    bisectDate = d3.bisector(function(d) { return d[0]; }).left,
    legendFormat = d3.time.format('%b %d, %Y');

    var x = d3.time.scale().range([0, width]),
    x2  = d3.time.scale().range([0, width]),
    y   = d3.scale.linear().range([height, 0]),
    y1  = d3.scale.linear().range([height, 0]),
    y2  = d3.scale.linear().range([height2, 0]),
    y3  = d3.scale.linear().range([60, 0]);

    var xAxis = d3.svg.axis().scale(x).orient('bottom'),
    xAxis2  = d3.svg.axis().scale(x2).orient('bottom'),
    yAxis   = d3.svg.axis().scale(y).orient('left');

    var priceLine = d3.svg.line()
    .interpolate('monotone')
    .x(function(d) { return x(d[0]); })
    .y(function(d) { return y(d[1]); });

    // var avgLine = d3.svg.line()
    // .interpolate('monotone')
    // .x(function(d) { return x(d.date); })
    // .y(function(d) { return y(d.average); });

  	var area2 = d3.svg.area()
    .interpolate('monotone')
    .x(function(d) { return x2(d[0]); })
    .y0(height2)
    .y1(function(d) { return y2(d[1]); });

    var svg = d3.select("#date-chart").append('svg')
    .attr('class', 'chart')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom + 60);

  	svg.append('defs').append('clipPath')
    .attr('id', 'clip')
  	.append('rect')
    .attr('width', width)
    .attr('height', height);

    var make_y_axis = function () {
    	return d3.svg.axis()
      .scale(y)
      .orient('left')
      .ticks(3);
  };

  var focus = svg.append('g')
    .attr('class', 'focus')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

  var barsGroup = svg.append('g')
    .attr('class', 'volume')
    .attr('clip-path', 'url(#clip)')
    .attr('transform', 'translate(' + margin.left + ',' + (margin.top + 60 + 20) + ')');

  var context = svg.append('g')
    .attr('class', 'context')
    .attr('transform', 'translate(' + margin2.left + ',' + (margin2.top + 60) + ')');

  var legend = svg.append('g')
    .attr('class', 'chart__legend')
    .attr('width', width)
    .attr('height', 30)
    .attr('transform', 'translate(' + margin2.left + ', 10)');

  legend.append('text')
    .attr('class', 'chart__symbol')
    .text('NASDAQ: AAPL')

  var rangeSelection =  legend
    .append('g')
    .attr('class', 'chart__range-selection')
    .attr('transform', 'translate(110, 0)');

  var brush = d3.svg.brush()
  .x(x2)
  .on('brush', brushed);

  var xRange = d3.extent(data.map(function(d) { return d[0]; }));

	x.domain(xRange);
	y.domain(d3.extent(data.map(function(d) { return d[1]; })));
	y3.domain(d3.extent(data.map(function(d) { return d[1]; })));
	x2.domain(x.domain());
	y2.domain(y.domain());

	var min = d3.min(data.map(function(d) { return d[1]; }));
    var max = d3.max(data.map(function(d) { return d[1]; }));

    var range = legend.append('text')
  .text(legendFormat(new Date(parseInt(xRange[0])*1000)) + ' - ' + legendFormat(new Date(parseInt(xRange[1])*1000)))
  .style('text-anchor', 'end')
  .attr('transform', 'translate(' + width + ', 0)');

  focus.append('g')
    .attr('class', 'y chart__grid')
    .call(make_y_axis()
    .tickSize(-width, 0, 0)
    .tickFormat(''));

    // var averageChart = focus.append('path')
    //     .datum(data)
    //     .attr('class', 'chart__line chart__average--focus line')
    //     .attr('d', avgLine);

    var priceChart = focus.append('path')
        .datum(data)
        .attr('class', 'chart__line chart__price--focus line')
        .attr('d', priceLine);

    focus.append('g')
        .attr('class', 'x axis')
        .attr('transform', 'translate(0 ,' + height + ')')
        .call(xAxis);

    focus.append('g')
        .attr('class', 'y axis')
        .attr('transform', 'translate(12, 0)')
        .call(yAxis);

    var focusGraph = barsGroup.selectAll('rect')
        .data(data)
      .enter().append('rect')
        .attr('class', 'chart__bars')
        .attr('x', function(d, i) { return x(d[0]); })
        .attr('y', function(d) { return 155 - y3(d[1]); })
        .attr('width', 1)
        .attr('height', function(d) { return y3(d[1]); });

    var helper = focus.append('g')
      .attr('class', 'chart__helper')
      .style('text-anchor', 'end')
      .attr('transform', 'translate(' + width + ', 0)');

    var helperText = helper.append('text')

    var priceTooltip = focus.append('g')
      .attr('class', 'chart__tooltip--price')
      .append('circle')
      .style('display', 'none')
      .attr('r', 2.5);

    var averageTooltip = focus.append('g')
      .attr('class', 'chart__tooltip--average')
      .append('circle')
      .style('display', 'none')
      .attr('r', 2.5);

    var mouseArea = svg.append('g')
      .attr('class', 'chart__mouse')
      .append('rect')
      .attr('class', 'chart__overlay')
      .attr('width', width)
      .attr('height', height)
      .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
      .on('mouseover', function() {
        helper.style('display', null);
        priceTooltip.style('display', null);
        // averageTooltip.style('display', null);
      })
      .on('mouseout', function() {
        helper.style('display', 'none');
        priceTooltip.style('display', 'none');
        // averageTooltip.style('display', 'none');
      })
      .on('mousemove', mousemove);

    // context.append('path')
    //     .datum(data)
    //     .attr('class', 'chart__area area')
    //     .attr('d', area2);

    context.append('g')
        .attr('class', 'x axis chart__axis--context')
        .attr('y', 0)
        .attr('transform', 'translate(0,' + (height2 - 22) + ')')
        .call(xAxis2);

    context.append('g')
        .attr('class', 'x brush')
        .call(brush)
      .selectAll('rect')
        .attr('y', -6)
        .attr('height', height2 + 7);

    function mousemove() {
      var x0 = x.invert(d3.mouse(this)[0]);
      console.log(x0);
      var i = bisectDate(data, x0, 1);
      // console.log(data.length);
      // console.log(i);
      var d0 = data[i - 1];
      var d1 = data[i];
      console.log(i);
      console.log(d0);
      console.log(d1);
      var d = x0 - d0[0] > d1[0] - x0 ? d1 : d0;
      helperText.text(legendFormat(new Date(parseInt(d[0])*1000)) + ' - Price: ' + d[1]);
      priceTooltip.attr('transform', 'translate(' + x(d[0]) + ',' + y(d[1]) + ')');
      // averageTooltip.attr('transform', 'translate(' + x(d[0]) + ')');
    }

    function brushed() {
      var ext = brush.extent();
      if (!brush.empty()) {
        x.domain(brush.empty() ? x2.domain() : brush.extent());
        y.domain([
          d3.min(data.map(function(d) { return (d[0] >= ext[0] && d[0] <= ext[1]) ? d[1] : max; })),
          d3.max(data.map(function(d) { return (d[0] >= ext[0] && d[0] <= ext[1]) ? d[1] : min; }))
        ]);
        range.text(legendFormat(new Date(ext[0])) + ' - ' + legendFormat(new Date(ext[1])))
        focusGraph.attr('x', function(d, i) { return x(d[0]); });

        var days = Math.ceil((ext[1] - ext[0]) / (24 * 3600 * 1000))
        focusGraph.attr('width', (40 > days) ? (40 - days) * 5 / 6 : 5)
      }
      priceChart.attr('d', priceLine);
      // averageChart.attr('d', avgLine);
      focus.select('.x.axis').call(xAxis);
      focus.select('.y.axis').call(yAxis);
    }

    // var dateRange = ['1w', '1m', '3m', '6m', '1y', '5y']
    var dateRange = ['1d', '1w', '1m']
    for (var i = 0, l = dateRange.length; i < l; i ++) {
      var v = dateRange[i];
      rangeSelection
        .append('text')
        .attr('class', 'chart__range-selection')
        .text(v)
        .attr('transform', 'translate(' + (18 * i) + ', 0)')
        .on('click', function(d) { focusOnRange(this.textContent); });
    }

    function focusOnRange(range) {
      var today = new Date(parseInt(data[data.length - 1][0])*1000)
      var ext = new Date(parseInt(data[data.length - 1][0])*1000)

      if (range === '1d')
        ext.setMonth(ext.getMonth() - 1)

      if (range === '1m')
        ext.setMonth(ext.getMonth() - 1)

      if (range === '1w')
      {
      			console.log(ext);
      	        ext.setDate(ext.getDate() - 7);
      	        console.log(ext);
      }

      if (range === '3m')
        ext.setMonth(ext.getMonth() - 3)

      if (range === '6m')
        ext.setMonth(ext.getMonth() - 6)

      if (range === '1y')
        ext.setFullYear(ext.getFullYear() - 1)

      if (range === '5y')
        ext.setFullYear(ext.getFullYear() - 5)

      brush.extent([ext, today])
      // console.log(brush);
      brushed()
      console.log("coming through");
      context.select('g.x.brush').call(brush.extent([ext, today]))
    }

};

