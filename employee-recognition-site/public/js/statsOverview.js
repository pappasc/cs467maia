function statsOverview(){

    google.charts.load('current', {'packages':['corechart']});

    function drawchart(req){
        var data = new google.visualization.DataTable();
        var awards = req;
        
        //Populate Data attributes
        data.addColumn('string', 'type');
        data.addColumn('number', 'value');
        
        for (var i=0; i < awards[0].length; i++){
            console.log(awards[0][i]);
            console.log(awards[1][i]);
            data.addRow([awards[0][i],awards[1][i]]);   
        }
        
        // Set chart options
        var options = {'title':'Percentage of awards by type',
                       //'is3D':true,
                       'pieHole': 0.3,
                       'width': 500,
                       'height': 500};

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(data,options);
    }
        
    //Ajax Call to get data from middleware
    $.ajax({
        url:'/stats/Overview',
        type: 'POST',
        contentType: 'application/json',
        data: {},
        success: function(result){
            console.log('result - ' + result);
            drawchart(result);   
        },
        error: function(){
            Error("Chart data loading error.");
        }
    });
}