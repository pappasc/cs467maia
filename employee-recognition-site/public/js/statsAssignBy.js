function statsAssignedBy(){

    google.charts.load('current', {'packages':['corechart', 'bar']});

    function drawchart(req){
        var data = new google.visualization.DataTable();
        var awards = req;
        
        data.addColumn('string', 'type');
        data.addColumn('number', 'value');
        
        for (var i=0; i < awards[0].length; i++){
            console.log(awards[0][i]);
            console.log(awards[1][i]);
            data.addRow([awards[0][i],awards[1][i]]);   
        }
        
        // Set chart options
        var options = {'title':'Number of awards Awarded By',
                       'is3D':true,
                       'width':500,
                       'height':500};

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(data,options);
    };
    
    function drawBars(req){
        var data = new google.visualization.DataTable();
        var awards = req;
        
        data.addColumn('string', 'Employee');
        data.addColumn('number', 'Week');
        data.addColumn('number', 'Month');
        
        for (var i=0; i < awards[0].length; i++){
            console.log('Bar['+i+']: ' + awards[0][i]+ '-'+awards[2][i]+'-'+awards[3][i]);
            data.addRow([awards[0][i],awards[2][i],awards[3][i]]);
        }
        
        var options = {
            chart: { 'title': 'Number of awards Awarded by Type', bold:2},
            hAxis: { 'title': 'Total awards by type', minValue:0,},
            vAxis: { 'title': 'Employee'},
            legend: { position: 'bottom'},
            bars: 'horizontal',
            width: 500,
            height: 500
        };
        
        var typeChart = new google.charts.Bar(document.getElementById('bar_div'));
        typeChart.draw(data, options);
        
    };
        
    $.ajax({
        url:'/stats/AwardedBy',
        type: 'POST',
        contentType: 'application/json',
        data: {},
        success: function(result){
            console.log('result - ' + result);
            drawchart(result);
            drawBars(result);
        },
        error: function(){
            Error("Chart data loading error.");
        }
    });
}