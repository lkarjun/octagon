function plot_pie(xValues, yValues, title){
    
    var barColors = ["#b91d47", "#00aba9"];
    var type = "pie"
    var data = {}
    new Chart("myChart", {
        type: "pie",
        data: {
            labels: xValues,
            datasets: [{
            backgroundColor: barColors,
            data: yValues
            }]
        },
    options: {
        title: {
                display: true,
                text: title
            }
        }
    })

}