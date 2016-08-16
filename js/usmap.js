var USMapModule = (function() {
    //votes per racial groups in the 2012 elections (source: http://projects.fivethirtyeight.com/2016-swing-the-election/)
    // This is used as the starting point for the control values
    var percent_vote_repub = {hispanic:29, black:7, wht_col:56, wht_non_col:62, asn_othr:67 };
    var percent_vote_dem = {hispanic:71, black:93, wht_col:44, wht_non_col:38, asn_othr:33 };
    //var percent_vote_repub = {hispanic:50, black:50, wht_col:50, wht_non_col:50, asn_othr:50 };
    //var percent_vote_dem = {hispanic:50, black:50, wht_col:50, wht_non_col:50, asn_othr:50 };
    
    //average historic voter turnout (1980-2012) is used for 2016 (Source: http://www.census.gov/data/tables/time-series/demo/voting-and-registration/voting-historical-time-series.html Table A6; http://www.census.gov/content/dam/Census/library/visualizations/time-series/demo/a6-presidential.jpg)
    var percent_voter_turnout = {hispanic:47.8, black:58.9, wht_col:65.2, wht_non_col:65.2, asn_othr:46.9 };
    //var percent_voter_turnout = {hispanic:100, black:100, wht_col:100, wht_non_col:100, asn_othr:100 };
    
    var elvoteobj_cached = null;
    var centerobj_cached = null;
    
    var hmargin = 10,
        vmargin = 10;
    var map_width = 900,
        map_height = 500;
    var state_width = 260,
        state_height = 320;
    var state_bar_width = 290,
        state_bar_height = 350; 
    var circscale = d3.scale.sqrt()
                    .domain([0, map_height])
                    .range([0, 30]);
    var path = d3.geo.path();
    var map_svg = d3.select("#map_div")
                    .append("svg")
                    .attr("width", map_width)
                    .attr("height", map_height);
    var map_g = map_svg.append("g")
                    .attr("width", map_width - hmargin)
                    .attr("height", map_height - vmargin)
                    .attr("transform", "translate(" + hmargin + "," + vmargin + ")");
    var state_svg = d3.select("#state_div")
                    .append("svg")
                    .attr("width", state_width)
                    .attr("height", state_height);
    var state_g = state_svg
                    .append("g")
                    .attr("width", state_width - hmargin)
                    .attr("height", state_height- vmargin)
                    .attr("transform", "translate(" + hmargin + "," + vmargin + ")");
    var state_bar_svg = d3.select("#state_bar_div")
                        .append("svg")
                        .attr("width", state_bar_width)
                        .attr("height", state_bar_height);
    var state_bar_g = state_bar_svg
                        .append("g")
                        .attr("width", state_bar_width - hmargin)
                        .attr("height", state_bar_height - vmargin)
                        .attr("transform", "translate(" + hmargin + "," + vmargin + ")");
    var state_stat_off = 40;
    var state_stat_line_ht = 30;
    /* state bar chart related */
    var chartMargin = {top: 20, right: 20, bottom: 30, left: 80};
    var chartWidth = state_bar_width - hmargin - chartMargin.left - chartMargin.right;
    var chartHeight = state_bar_height - vmargin - chartMargin.top - chartMargin.bottom;
    var chartColor = d3.scale.ordinal()
                        .domain(["Dems", "Repub"])
                        .range(["steelblue", "indianred"]);
    var xScale = d3.scale.ordinal()
                        .domain(["Dems", "Repub"])
                        .rangeRoundBands([0, chartWidth], .1);
    var xAxis = d3.svg.axis()
                    .scale(xScale)
                    .orient("bottom");

    
    function zeroPad(num, places) {
        var zero = places - num.toString().length + 1;
        return Array(+(zero > 0 && zero)).join("0") + num;
    }
    function format_millions(num) {
        var num_mill = Math.floor(num / 1000000);
        var num_hunthou = Math.floor((num - num_mill * 1000000)/1000);
        var num_thou = Math.floor(num - (num_mill * 1000000) - (num_hunthou * 1000));
        num_str = "";
        if (num_mill != 0)
            num_str = num_str + num_mill.toString() + "," ;
        if (num_mill != 0 || num_hunthou != 0)
            num_str = num_str + zeroPad(num_hunthou, 3) + ",";
            num_str = num_str + zeroPad(num_thou, 3);
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
    
    function compute_popular_vote(propobj) {
        propobj.repub_votes = (propobj.hispanic*0.01 * percent_vote_repub.hispanic*0.01 * percent_voter_turnout.hispanic*0.01 * propobj.population) +
                        (propobj.college_white*0.01 * percent_vote_repub.wht_col*0.01 * percent_voter_turnout.wht_col*0.01 * propobj.population) +
                        (propobj.noncollege_white*0.01 * percent_vote_repub.wht_non_col*0.01 * percent_voter_turnout.wht_non_col*0.01 * propobj.population) +
                        (propobj.black*0.01 * percent_vote_repub.black*0.01 * percent_voter_turnout.black*0.01 * propobj.population) +
                        (propobj.asian_other*0.01 * percent_vote_repub.asn_othr*0.01 * percent_voter_turnout.asn_othr*0.01 * propobj.population);
           

        propobj.dem_votes = (propobj.hispanic*0.01 * percent_vote_dem.hispanic*0.01 * percent_voter_turnout.hispanic*0.01 * propobj.population) +
            (propobj.college_white*0.01 * percent_vote_dem.wht_col*0.01 * percent_voter_turnout.wht_col*0.01 * propobj.population) +
            (propobj.noncollege_white*0.01 * percent_vote_dem.wht_non_col*0.01 * percent_voter_turnout.wht_non_col*0.01 * propobj.population) +
            (propobj.black*0.01 * percent_vote_dem.black*0.01 * percent_voter_turnout.black*0.01 * propobj.population) +
            (propobj.asian_other*0.01 * percent_vote_dem.asn_othr*0.01 * percent_voter_turnout.asn_othr*0.01 * propobj.population);
        
        propobj.repub_votes = Math.round(propobj.repub_votes);
        propobj.dem_votes = Math.round(propobj.dem_votes);
    }
    
    function stateClick(stateobj) {
            state_svg
                .selectAll(".ststats")
                .remove();
            state_bar_svg
                .selectAll(".stbar_title")
                .remove();
            state_bar_svg
                .selectAll(".stbar")
                .remove();
            var max_pop = 0;

            state_text = state_svg.selectAll(".ststats")
                            .data(elvoteobj_cached.features.filter(function (d) { return d.id == stateobj.id;}))
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
                            max_pop = d.properties.dem_votes + d.properties.repub_votes;
                            return d.properties.name;
                        })
                .attr("x", state_stat_off)
                .attr("y", compute_stat_height(1));
            state_text.
                append("tspan")
                .attr("class", "state_stat_stats")
                .text(function(d) {
                            return "Population: " + format_millions(d.properties.population);
                        })
                .attr("x", state_stat_off)
                .attr("y", compute_stat_height(2));
            state_text.
                append("tspan")
                .attr("class", "state_stat_stats")
                .text(function(d) {
                            return "College educated white: " + d.properties.college_white + "%";
                        })
                .attr("x", state_stat_off)
                .attr("y", compute_stat_height(3));	
            state_text.
                append("tspan")
                .attr("class", "state_stat_stats")
                .text(function(d) {
                            return "Non-College white: " + d.properties.noncollege_white + "%";
                        })
                .attr("x", state_stat_off)
                .attr("y", compute_stat_height(4));	
            state_text.
                append("tspan")
                .attr("class", "state_stat_stats")
                .text(function(d) {
                            return "African American: " + d.properties.black + "%";
                        })
                .attr("x", state_stat_off)
                .attr("y", compute_stat_height(5));	
            state_text.
                append("tspan")
                .attr("class", "state_stat_stats")
                .text(function(d) {
                            return "Hispanic: " + d.properties.hispanic + "%";
                        })
                .attr("x", state_stat_off)
                .attr("y", compute_stat_height(6));	
            state_text.
                append("tspan")
                .attr("class", "state_stat_stats")
                .text(function(d) {
                            return "Asian/other: " + d.properties.asian_other + "%";
                        })
                .attr("x", state_stat_off)
                .attr("y", compute_stat_height(7));	
            state_text.
                append("tspan")
                .attr("class", "state_stat_stats")
                .text(function(d) {
                            winner = ""
                            if (d.properties.dem_votes > d.properties.repub_votes) {
                                winner = " (WIN)"
                            }
                            return "Democratic Vote: " + format_millions(d.properties.dem_votes) + winner;
                        })
                .attr("x", state_stat_off)
                .attr("y", compute_stat_height(8));
            state_text.
                append("tspan")
                .attr("class", "state_stat_stats")
                .text(function(d) {
                            winner = ""
                            if (d.properties.repub_votes > d.properties.dem_votes) {
                                winner = " (WIN)"
                            }
                            return "Republican Vote: " + format_millions(d.properties.repub_votes) + winner;
                        })
                .attr("x", state_stat_off)
                .attr("y", compute_stat_height(9));
            state_text.
                append("tspan")
                .attr("class", "state_stat_stats")
                .text(function(d) {
                            return "Electoral Seats: " + d.properties.electoral;
                        })
                .attr("x", state_stat_off)
                .attr("y", compute_stat_height(10));


            
            /*console.log(stateobj.id); */
            var yScale = d3.scale.linear()
                    .domain([0, max_pop])
                    .range([chartHeight - 100, 0]);
            var state_pop_ticks = [];
            for (l = 0; l < max_pop; l += 5000000) {
                state_pop_ticks.push(l);
            }
            var yAxis = d3.svg.axis()
                            .scale(yScale)
                            .orient("left")
                            .tickValues(state_pop_ticks)
                            .tickFormat(function(d) { return d / 1000000;});
            state_bar_stats = state_bar_g.selectAll(".stbar_title")
                            .data(elvoteobj_cached.features.filter(function (d) { return d.id == stateobj.id;}))
                            .enter()
                            .append("g")
                            .attr("class", "stbar_title")
                            .attr("transform", "translate(" + 100 + ",0)");
            state_bar_stats.append("text")
                            .text("Popular Vote")
                            .attr("class", "state_bar_title")
                            .attr("x", 30)
                            .attr("y", 30)
                            .attr("width", 100)
                            .attr("height", 100);

            state_bar_chart = state_bar_g.selectAll(".stbar")
                            .data(elvoteobj_cached.features.filter(function (d) { return d.id == stateobj.id;}))
                            .enter()
                            .append("g")
                            .attr("class", "stbar");
            state_bar_chart.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(100," + chartHeight + ")")
                .call(xAxis);
            state_bar_chart.append("g")
                .attr("class", "y axis")
                .attr("transform", "translate(100," + 100 + ")")
                .call(yAxis);
            cur_state = elvoteobj_cached.features.filter(function (d) { return d.id == stateobj.id;})
            state_bar_chart.selectAll(".state_bar")
                .data([cur_state[0].properties.dem_votes, cur_state[0].properties.repub_votes])
                .enter()
                .append("rect")
                .attr("class", "state_bar")
                .attr("x", function(d, i) { if (i == 0) return xScale("Dems"); else return xScale("Repub");})
                .attr("width", xScale.rangeBand())
                .attr("y", function(d) { return yScale(d); })
                .attr("height", function(d) { return chartHeight - yScale(d) - 100; })
                .attr("title", function(d) {return d + " votes"; })
                .style("fill", function(d, i) { if (i == 0) return chartColor("Dems"); else return chartColor("Repub");})
                .attr("transform", "translate(" + 100 + "," + 100 + ")");

        }
    
    
    function updateTally(dem_tally, repub_tally) {
        d3.select("#dem_tally").text(dem_tally);
        d3.select("#repub_tally").text(repub_tally);
        if(dem_tally > repub_tally) {
            d3.select("#dem_winner").style("opacity", 1);;
            d3.select("#repub_winner").style("opacity", 0);;
        }
        else if(repub_tally > dem_tally){
            d3.select("#dem_winner").style("opacity", 0);;
            d3.select("#repub_winner").style("opacity", 1);;
        }
        
    }
    function data_loaded(error, usobj, elvoteobj, centerobj, labelobj, ptrobj) {
        if (error) throw error;

        var repub_tally = 0, dem_tally = 0;
        
        for (i = 0; i < centerobj.features.length; i++) {
            for (j = 0; j < elvoteobj.features.length; j++) {
                if (elvoteobj.features[j].id == centerobj.features[i].id) {
                    if (centerobj.features[i].elvotes != null)
                        throw "Data Corruption";
                    else

                        centerobjprops = centerobj.features[i].properties;
                        labelobjprops = labelobj.features[i].properties;
                        elvoteobjprops = elvoteobj.features[j].properties;
                    
                        centerobjprops.elvotes = labelobjprops.elvotes = Number(elvoteobjprops.electoral);
                        
                        compute_popular_vote(elvoteobjprops);
                        
                        centerobjprops.repub_votes = elvoteobjprops.repub_votes = Math.round(elvoteobjprops.repub_votes);
                        centerobjprops.dem_votes = elvoteobjprops.dem_votes = Math.round(elvoteobjprops.dem_votes);
                        
                        if(elvoteobjprops.dem_votes > elvoteobjprops.repub_votes){
                            dem_tally += elvoteobjprops.electoral;
                        }
                        else if(elvoteobjprops.repub_votes > elvoteobjprops.dem_votes){
                            repub_tally += elvoteobjprops.electoral;
                        }
                    
                        console.log(elvoteobjprops.name + "," + elvoteobjprops.population + "," + elvoteobjprops.electoral + "," 
                                    + elvoteobjprops.dem_votes + "," + elvoteobjprops.repub_votes);
                    
                    break;
                }
            }
        }
        updateTally(dem_tally, repub_tally);
                
        map_svg
            .selectAll("path")
            .data(topojson.feature(usobj, usobj.objects.states).features)
            .enter()
            .append("path")
            .attr("class", "state")
            .attr("d", path)
            .on('mouseover', function(d) {d3.select(this).style("cursor", "pointer").classed("distinct", true)})
            .on('mouseout', function(d) {d3.select(this).style("cursor", "default").classed("distinct", false);})
            .on('mousedown', function(d) {
               d3.selectAll(".state").classed("selected", false);
               d3.select(this).classed("distinct", false);
               d3.select(this).classed("selected", true);
               stateClick(d);
            });

        map_svg
            .selectAll(".circle")
            .data(centerobj.features)
            .enter()
            .append("path")
            .attr("class", function(d) { if (d.properties.dem_votes > d.properties.repub_votes) {
                                            return "circle dem_circle";
                                        } 
                                        else if (d.properties.repub_votes > d.properties.dem_votes) {
                                            return "circle rep_circle";
                                        }
                                        else {
                                            return "circle split_circle";
                                        }
                                    })
            .attr("d", path.pointRadius(function(d) {return circscale(Math.pow(d.properties.elvotes,2)); }))
            .on('mouseover', function(d) {
                d3.select(this).style("cursor", "pointer");
                cur_circle = d;
                cur_state = d3.selectAll(".state").filter(function(d) { return d.id == cur_circle.id; });
                cur_state.classed("distinct", true);
            })
            .on('mouseout', function(d) {
                d3.select(this).style("cursor", "default");
                cur_circle = d;
                cur_state = d3.selectAll(".state").filter(function(d) { return d.id == cur_circle.id; });
                cur_state.classed("distinct", false);
            })
            .on('mousedown', function(d) {
                cur_circle = d;
                d3.selectAll(".state").classed("selected", false);
                cur_state = d3.selectAll(".state").filter(function(d) { return d.id == cur_circle.id; });
                cur_state.classed("distinct", false);
                cur_state.classed("selected", true);
                stateClick(cur_state.data()[0]);
            });
        map_svg.selectAll("text")
            .data(labelobj.features)
            .enter()
            .append("text")
            .attr("class", "label")
            .text(function(d) { return d.properties.abbrev; })
            .attr("x", function(d) { return path.centroid(d)[0]; })
            .attr("y", function(d) { return path.centroid(d)[1]; })
            .on('mouseover', function(d) {
                d3.select(this).style("cursor", "pointer");
                cur_label = d;
                cur_state = d3.selectAll(".state").filter(function(d) { return d.id == cur_label.id; });
                cur_state.classed("distinct", true);
            })
            .on('mouseout', function(d) {
                d3.select(this).style("cursor", "default");
                cur_label = d;
                cur_state = d3.selectAll(".state").filter(function(d) { return d.id == cur_label.id; });
                cur_state.classed("distinct", false);
            })
            .on('mousedown', function(d) {
                cur_label = d;
                d3.selectAll(".state").classed("selected", false);
                cur_state = d3.selectAll(".state").filter(function(d) { return d.id == cur_label.id; });
                cur_state.classed("distinct", false);
                cur_state.classed("selected", true);
                stateClick(cur_state.data()[0]);
            });
        map_svg.selectAll(".ptr")
            .data(ptrobj.features)
            .enter()
            .append("path")
            .attr("class", "ptr")
            .attr("d", path);

        //cache the core data object
        elvoteobj_cached = elvoteobj;
        centerobj_cached = centerobj;
        
    }// end function data_loaded
    
    return {
        initialize: function() {
                console.log("Inside Map Initialize");
                queue()
                .defer(d3.json, "us.json")
                .defer(d3.json, "pop_new.json")
                .defer(d3.json, "center-adj.json")
                .defer(d3.json, "label-adj.json")
                .defer(d3.json, "ptr-adj.json")
                .await(data_loaded);
        },
        
        updateVotePct: function(value){
            console.log("inside updateVotePct");
            console.log(value);
            if(value.item == "hispanic") {
                percent_vote_repub.hispanic = Number(value.vote_repub);
                percent_vote_dem.hispanic = 100 - Number(value.vote_repub);
            }
            else if(value.item == "college"){
                percent_vote_repub.wht_col = Number(value.vote_repub);
                percent_vote_dem.wht_col = 100 - Number(value.vote_repub);
            }
            else if(value.item == "no_college") {
                percent_vote_repub.wht_non_col = Number(value.vote_repub);
                percent_vote_dem.wht_non_col = 100 - Number(value.vote_repub);
            }
            else if(value.item == "afro") {
                percent_vote_repub.black = Number(value.vote_repub);
                percent_vote_dem.black = 100 - Number(value.vote_repub);
            }
            else if(value.item == "asian"){
                percent_vote_repub.asn_othr = Number(value.vote_repub);
                percent_vote_dem.asn_othr = 100 - Number(value.vote_repub);
            }
            
            var dem_tally = 0, repub_tally = 0;
            
            for (ii = 0; ii < elvoteobj_cached.features.length; ii++) {
                elvoteobjprops = elvoteobj_cached.features[ii].properties;
                compute_popular_vote(elvoteobjprops);
                
                for (jj = 0; jj < centerobj_cached.features.length; jj++) {
                    if (elvoteobj_cached.features[ii].id == centerobj_cached.features[jj].id) {
                        centerobj_cached.features[jj].properties.repub_votes = elvoteobjprops.repub_votes;
                        centerobj_cached.features[jj].properties.dem_votes = elvoteobjprops.dem_votes;
                        break;
                    }
                }
                
                if(elvoteobjprops.dem_votes > elvoteobjprops.repub_votes){
                    dem_tally += elvoteobjprops.electoral;
                }
                else if(elvoteobjprops.repub_votes > elvoteobjprops.dem_votes){
                    repub_tally += elvoteobjprops.electoral;
                }

                //console.log(elvoteobjprops.name + "," + elvoteobjprops.population + "," + elvoteobjprops.electoral + "," 
                //                    + elvoteobjprops.dem_votes + "," + elvoteobjprops.repub_votes);
            }
            
            updateTally(dem_tally, repub_tally);
            
            /*
            circles = map_svg.selectAll(".circle")
                    .data(centerobj_cached.features);
            console.log("Circles:");
            console.log(circles);
            
            dem_to_repub = map_svg.selectAll(".circle.dem_circle")
                .filter(function(d){return d.properties.dem_votes < d.properties.repub_votes});
            console.log("demtorepub:");
            console.log(dem_to_repub);
            
            repub_to_dem = map_svg.selectAll(".circle.repub_circle");
                //.filter(function(d){return d.properties.dem_votes > d.properties.repub_votes});
            console.log("repubtodem");
            console.log(repub_to_dem);
            
            dem_to_repub
                .classed("dem_circle", "false")
                .classed("split_circle")
                .classed("repub_circle", "true");

            repub_to_dem
                .classed("repub_circle", "false")
                .classed("split_circle")
                .classed("dem_circle", "true");
                */
            map_svg
            .selectAll(".circle")
            .data(centerobj_cached.features)
            .attr("class", function(d) { if (d.properties.dem_votes > d.properties.repub_votes) {
                                            return "circle dem_circle";
                                        } 
                                        else if (d.properties.repub_votes > d.properties.dem_votes) {
                                            return "circle rep_circle";
                                        }
                                        else {
                                            return "circle split_circle";
                                        }
                                    });

                
        },//end function updateVotePct
        
        clearStateStats :   function ()
        {
            state_svg
                .selectAll(".ststats")
                .remove();
            state_bar_svg
                .selectAll(".stbar_title")
                .remove();
            state_bar_svg
                .selectAll(".stbar")
                .remove();
            map_svg.selectAll("path")
                .classed("distinct", false)
                .classed("selected", false);
            map_svg.selectAll("text")
                .classed("distinct", false)
                .classed("selected", false);
        }
    }
}())//end USMapModule


USMapModule.initialize();
//USMapModule.updateVotePct({item:"hispanic", vote_rep:0.8});
