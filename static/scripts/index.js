var socket = io();


socket.on('connect', function() {
                socket.emit('get_data', {'data': 'I\'m connected!'});
 });
socket.on('data', function(data){
	 createChart(data);
});


function createChart(jsonData){
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(function(){
	drawChart(jsonData)
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

