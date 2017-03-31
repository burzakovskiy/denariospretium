var socket = io();

var pair = "BTC_DASH";
var chartData={};
google.charts.load('current', {'packages':['corechart']});



socket.on('connect', function() {
	socket.emit('get_data', {'data': 'I\'m connected!'});
});

socket.on('data', function(data){
	 chartData = data;
	 document.getElementById("pairHeader").innerHTML =getPairNameByID(pair)+" price forecast" ;
	 updateTwitterFeed(pair);
	 createChart(chartData[pair]);
});


function updatePair(input){
	pair= input;
	document.getElementById("pairHeader").innerHTML =getPairNameByID(pair)+" price forecast" ;
	updateTwitterFeed(pair);
	createChart(chartData[pair]);
}

function updateTwitterFeed(pair){
	var wrap = document.getElementById("twitterWrapper");
	while (wrap.hasChildNodes()) {
    	wrap.removeChild(wrap.lastChild);
	}
	if(document.getElementById("twitter-wjs")){
		var p = document.getElementsByTagName("head")[0];
		var c= document.getElementById("twitter-wjs");
		p.removeChild(c);
	}
	
	var link = document.createElement("a");
	link.setAttribute("class", "twitter-timeline");
	switch(pair){
		case "BTC_DASH":
			
			link.setAttribute("href", "https://twitter.com/hashtag/dash");
			link.setAttribute("data-widget-id", "847400652619751424");
			break;
		case "BTC_ETH":
			link.setAttribute("href", "https://twitter.com/hashtag/Ethereum");
			link.setAttribute("data-widget-id", "847756593789779968");
			break;
		case "BTC_XMR":
			link.setAttribute("href", "https://twitter.com/hashtag/Monero");
			link.setAttribute("data-widget-id", "847757181776736256");
			break;
	}
	wrap.appendChild(link);
	!function(d,s,id){
	var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';
	if(!d.getElementById(id)){
		js=d.createElement(s);
		js.id=id;
		js.src=p+"://platform.twitter.com/widgets.js";
		fjs.parentNode.insertBefore(js,fjs);
		}
	}(document,"script","twitter-wjs");
	
}
function createChart(jsonData){
	google.charts.setOnLoadCallback(function(){
		drawChart(jsonData);
	});	
}


function drawChart(jsonData) {
	var data = new google.visualization.DataTable(jsonData);
    data.addColumn('datetime', 'Date');
    data.addColumn('number', 'Price');
	for (var key in jsonData){
    	data.addRow([new Date(key*1000), jsonData[key]]);
    }
      var options = {
        hAxis: {
         
       	  textStyle:{
           color: '#FFFFFF'
          },
          titleTextStyle: {
          color: '#FFFFFF'
        	}
        },
        vAxis: {
         
          titleTextStyle: {
          color: '#FFFFFF'
        	},
           textStyle:{
           color: '#FFFFFF'
          },
        },
        legend:{position:'none'},
        backgroundColor: '#292f33',
        
      };


    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

    chart.draw(data, options);
      }

function getPairNameByID(id){
	switch(id){
		case "BTC_DASH":
			return "DASHBTC";
		case "BTC_ETH":
			return "ETHBTC";
		case "BTC_XMR":
			return "XMRBTC";
	}
}