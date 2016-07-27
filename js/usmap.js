var hmargin = 10,
    vmargin = 10;

var map_width = 900,
    map_height = 500;

var state_width = 900,
	state_height = 500;

var circscale = d3.scale.sqrt()
				.domain([0, map_height])
				.range([0, 30]);

var path = d3.geo.path();

var map_box = d3.select("#map_div")
				.append("g")
				.attr("width", map_width)
				.attr("height", map_height);

var mapsvg = map_box.append("svg")
				.attr("width", map_width - hmargin)
				.attr("height", map_height - vmargin)
				.attr("transform", "translate(" + hmargin + "," + vmargin + ")")
                .attr("class", "img-responsive");

var state_box = d3.select("#state_div")
					.append("g")
					.attr("width", state_width)
					.attr("height", state_height);

var statesvg = state_box.append("svg")
				.attr("width", state_width - hmargin)
				.attr("height", state_height - vmargin)
				.attr("transform", "translate(" + hmargin + "," + vmargin + ")");

var state_stat_off = 40;

var state_stat_line_ht = 30

queue()
	.defer(d3.json, "us.json")
	.defer(d3.json, "pop.json")
	.defer(d3.json, "center-adj.json")
	.defer(d3.json, "label-adj.json")
	.defer(d3.json, "ptr-adj.json")
	.await(data_loaded);

function format_millions(num) {
	var num_mill = Math.floor(num / 1000000);
	var num_hunthou = Math.floor((num - num_mill * 1000000)/1000);
	var num_thou = Math.floor(num - (num_mill * 1000000) - (num_hunthou * 1000));
	num_str = "";
	if (num_mill != 0)
		num_str = num_str + num_mill.toString() + "," ;
	if (num_mill != 0 || num_hunthou != 0)
		num_str = num_str + num_hunthou.toString() + ",";

	num_str = num_str + num_thou.toString();

	return num_str;
}

function compute_stat_height(line_num) {
	return state_stat_off + (line_num - 1) * state_stat_line_ht;

}

function compute_party_electoral(electoral, pct, complement) {
	pelec = Math.floor(electoral * (pct / 100))
	if (complement) {
		return electoral - pelec;
	} else {
		return pelec;
	}

}

function data_loaded(error, usobj, elvoteobj, centerobj, labelobj, ptrobj) {
	if (error) throw error;

	for (i = 0; i < centerobj.features.length; i++) {
		for (j = 0; j < elvoteobj.features.length; j++) {
			if (elvoteobj.features[j].id == centerobj.features[i].id) {
				if (centerobj.features[i].elvotes != null)
					throw "Data Corruption";
				else
					centerobj.features[i].properties.elvotes = labelobj.features[i].properties.elvotes = Number(elvoteobj.features[j].properties.electoral);
					centerobj.features[i].properties.pop12 = elvoteobj.features[j].properties.pop12;
					console.log(elvoteobj.features[j].properties.name + "," + elvoteobj.features[j].properties.population + "," + elvoteobj.features[j].properties.electoral);
				break;
			}
		}

	}

	mapsvg
		.selectAll("path")
		.data(topojson.feature(usobj, usobj.objects.states).features)
		.enter()
		.append("path")
		.attr("class", "state")
		.attr("d", path)
		.on('mousedown', function(d) {
		   d3.selectAll(".state").classed("selected", false);
		   d3.select(this).classed("selected", true);
		   stateClick(d);
		});

	mapsvg
		.selectAll(".circle")
		.data(centerobj.features)
		.enter()
		.append("path")
		.attr("class", function(d) { if (d.properties.pop12[0] > d.properties.pop12[1]) {
										return "dem_circle";
									} else {
										return "rep_circle";
									}
								})
		.attr("d", path.pointRadius(function(d) {return circscale(Math.pow(d.properties.elvotes,2)); }));

	mapsvg.selectAll("text")
		.data(labelobj.features)
		.enter()
		.append("text")
		.attr("class", "label")
		.text(function(d) { return d.properties.abbrev; })
		.attr("x", function(d) { return path.centroid(d)[0]; })
		.attr("y", function(d) { return path.centroid(d)[1]; });

	mapsvg.selectAll(".ptr")
		.data(ptrobj.features)
		.enter()
		.append("path")
		.attr("class", "ptr")
		.attr("d", path);

	

	function stateClick(stateobj) {

		statesvg
			.selectAll(".ststats")
			.remove();
		
		state_text = statesvg.selectAll(".ststats")
						.data(elvoteobj.features.filter(function (d) { return d.id == stateobj.id;}))
						.enter()
						.append("text")
						.text(null)
						.attr("class", "ststats")
						.attr("x", state_stat_off)
						.attr("y", state_stat_off);

		state_text.
			append("tspan")
			.attr("class", "state_stat_hdr")
			.text(function(d) {
						return d.properties.name;
					})
			.attr("x", state_stat_off)
			.attr("y", compute_stat_height(1));

		state_text.
			append("tspan")
			.attr("class", "state_stat_stats")
			.text(function(d) {
				        return "Democratic Pop Vote: " + format_millions(d.properties.pop12[0]);
					})
			.attr("x", state_stat_off)
			.attr("y", compute_stat_height(2));

		state_text.
			append("tspan")
			.attr("class", "state_stat_stats")
			.text(function(d) {
				        return "Republican Pop Vote: " + format_millions(d.properties.pop12[1]);
					})
			.attr("x", state_stat_off)
			.attr("y", compute_stat_height(3));
			

		state_text.
			append("tspan")
			.attr("class", "state_stat_stats")
			.text(function(d) {
						if (d.properties.pop12[0] > d.properties.pop12[1]) {
				        	return "EC Votes awarded to: Democrats (Obama)";
						} else {
							return "EC Votes awarded to: Republicans (Romney)";
						}
					})
			.attr("x", state_stat_off)
			.attr("y", compute_stat_height(4));

		state_text.
			append("tspan")
			.attr("class", "state_stat_stats")
			.text(function(d) {
				        return "EC Votes awarded: " + d.properties.electoral;
					})
			.attr("x", state_stat_off)
			.attr("y", compute_stat_height(5));		
		/*console.log(stateobj.id); */
	}


}