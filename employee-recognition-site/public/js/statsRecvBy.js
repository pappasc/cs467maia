function statsRecvBy(){

    google.charts.load('current', {'packages':['corechart']});

    function drawchart(req){
        var data = new google.visualization.DataTable();
        var awards = req;
        
        data.addColumn('string', 'type');
        data.addColumn('number', 'value');
        
        for (var i=0; i < awards[0].length; i++){
            console.log(awards[0][i]);
            data.addRow([awards[0][i],awards[1][i]]);   
        }
        
        // Set chart options
        var options = {'title':'Number of awards Received By',
                       'is3D': true,
                       'width':600,
                       'height':600};

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(data,options);
    }
    
    $.ajax({
        url:'/stats/RecvBy',
        type: 'POST',
        contentType: 'application/json',
        data: {},
        success: function(result){
            console.log(result);
            drawchart(result);   
        },
        error: function(){
            Error("Chart data loading error.");
        }
    });
}
