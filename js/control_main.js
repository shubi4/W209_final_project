//Function that call the right page
	function actionCall(year){
		if (year == 2016)
			document.getElementById('anchor_2016').click();
		else if (year == 2012)
			document.getElementById('anchor_2012').click();
		else if (year == 2008)
			document.getElementById('anchor_2008').click();
	}
		

function control_main(id_menu){		
		var m = [80, 80, 80, 80]; // margins
		var w = 1000 - m[1] - m[3]; // width
		var h = 550 - m[0] - m[2]; // height
		
		var democrats = [266, 251, 365, 332, 332];
		var republicans = [271, 286, 173, 206, 206];

		var x = d3.scale.linear().domain([0, 4]).range([0, w]);
		
		var y = d3.scale.linear().domain([0, 400]).range([h, 0]);
		var line = d3.svg.line()
			.x(function(d,i) {return x(i)})
			.y(function(d) {return y(d)});
		
		var main_menu = d3.select(id_menu).append("svg:svg")
			  .attr("width", w + m[1] + m[3])
			  .attr("height", h + m[0] + m[2])
			  .append("svg:g")
			  .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

		var xAxis = d3.svg.axis()
					.scale(x)
					.ticks(5)
					.orient("bottom")
					.tickFormat(function(d) {
						if (d == 4)
							return "2016" ;
						else 
							return 4 * d + 2000;
					});

		var xa = main_menu.append("svg:g")
			  .attr("class", "x axis")
			  .attr("transform", "translate(0," + (h + 10) + ")")
			  .call(xAxis);
			
		var yAxisLeft = d3.svg.axis()
						.scale(y)
						.ticks(4)
						.orient("left")
						.innerTickSize(-w)
						.outerTickSize(0)
						.tickPadding(10);
						
		var ya = main_menu.append("svg:g")
			  .attr("class", "y axis")
			  .attr("transform", "translate(-25,0)")
			  .call(yAxisLeft);
				
		d3.selectAll(".tick > text")
		.attr("class", function(d) { 
				if ((d <=1) || (d >= 100))
					return "text_normal";
				else
					return "text_link";
				})
		.on('click',function(d) {
				if ((d > 1) && (d < 5))
					actionCall(4 * d + 2000);
		});

		main_menu.append("svg:path").attr("d", line(democrats)).attr("class","path1");
		main_menu.append("svg:path").attr("d", line(republicans)).attr("class","path2");
}

control_main("#main_menu");