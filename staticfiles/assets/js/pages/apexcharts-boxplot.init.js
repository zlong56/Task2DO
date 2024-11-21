function getChartColorsArray(t) {
    if (null !== document.getElementById(t)) return t = document.getElementById(t).getAttribute("data-colors"), (t = JSON.parse(t)).map(function(t) {
        var o = t.replace(" ", "");
        return -1 === o.indexOf(",") ? getComputedStyle(document.documentElement).getPropertyValue(o) || o : 2 == (t = t.split(",")).length ? "rgba(" + getComputedStyle(document.documentElement).getPropertyValue(t[0]) + "," + t[1] + ")" : o
    })
}
var options, chart, chartBoxBasicColors = getChartColorsArray("basic_box"),
    chartBoxPlotColors = (chartBoxBasicColors && (options = {
        series: [{
            type: "boxPlot",
            data: [{
                x: "Jan 2015",
                y: [54, 66, 69, 75, 88]
            }, {
                x: "Jan 2016",
                y: [43, 65, 69, 76, 81]
            }, {
                x: "Jan 2017",
                y: [31, 39, 45, 51, 59]
            }, {
                x: "Jan 2018",
                y: [39, 46, 55, 65, 71]
            }, {
                x: "Jan 2019",
                y: [29, 31, 35, 39, 44]
            }, {
                x: "Jan 2020",
                y: [41, 49, 58, 61, 67]
            }, {
                x: "Jan 2021",
                y: [54, 59, 66, 71, 88]
            }]
        }],
        chart: {
            type: "boxPlot",
            height: 350,
            toolbar: {
                show: !1
            }
        },
        title: {
            text: "Basic BoxPlot Chart",
            align: "left",
            style: {
                fontWeight: 500
            }
        },
        plotOptions: {
            boxPlot: {
                colors: {
                    upper: chartBoxBasicColors[0],
                    lower: chartBoxBasicColors[1]
                }
            }
        },
        stroke: {
            colors: [chartBoxBasicColors[2]]
        }
    }, (chart = new ApexCharts(document.querySelector("#basic_box"), options)).render()), getChartColorsArray("box_plot")),
    chartBoxPlotHoriColors = (chartBoxPlotColors && (options = {
        series: [{
            name: "Box",
            type: "boxPlot",
            data: [{
                x: new Date("2017-01-01").getTime(),
                y: [54, 66, 69, 75, 88]
            }, {
                x: new Date("2018-01-01").getTime(),
                y: [43, 65, 69, 76, 81]
            }, {
                x: new Date("2019-01-01").getTime(),
                y: [31, 39, 45, 51, 59]
            }, {
                x: new Date("2020-01-01").getTime(),
                y: [39, 46, 55, 65, 71]
            }, {
                x: new Date("2021-01-01").getTime(),
                y: [29, 31, 35, 39, 44]
            }]
        }, {
            name: "Outliers",
            type: "scatter",
            data: [{
                x: new Date("2017-01-01").getTime(),
                y: 32
            }, {
                x: new Date("2018-01-01").getTime(),
                y: 25
            }, {
                x: new Date("2019-01-01").getTime(),
                y: 64
            }, {
                x: new Date("2020-01-01").getTime(),
                y: 27
            }, {
                x: new Date("2020-01-01").getTime(),
                y: 78
            }, {
                x: new Date("2021-01-01").getTime(),
                y: 15
            }]
        }],
        chart: {
            type: "boxPlot",
            height: 350,
            toolbar: {
                show: !1
            }
        },
        colors: [chartBoxPlotColors[0], chartBoxPlotColors[1]],
        title: {
            text: "BoxPlot - Scatter Chart",
            align: "left",
            style: {
                fontWeight: 500
            }
        },
        xaxis: {
            type: "datetime",
            tooltip: {
                formatter: function(t) {
                    return new Date(t).getFullYear()
                }
            }
        },
        plotOptions: {
            boxPlot: {
                colors: {
                    upper: chartBoxPlotColors[2],
                    lower: chartBoxPlotColors[3]
                }
            }
        },
        stroke: {
            colors: [chartBoxPlotColors[4]]
        },
        tooltip: {
            shared: !1,
            intersect: !0
        }
    }, (chart = new ApexCharts(document.querySelector("#box_plot"), options)).render()), getChartColorsArray("box_plot_hori"));
chartBoxPlotHoriColors && (options = {
    series: [{
        data: [{
            x: "Category A",
            y: [54, 66, 69, 75, 88]
        }, {
            x: "Category B",
            y: [43, 65, 69, 76, 81]
        }, {
            x: "Category C",
            y: [31, 39, 45, 51, 59]
        }, {
            x: "Category D",
            y: [39, 46, 55, 65, 71]
        }, {
            x: "Category E",
            y: [29, 31, 35, 39, 44]
        }, {
            x: "Category F",
            y: [41, 49, 58, 61, 67]
        }, {
            x: "Category G",
            y: [54, 59, 66, 71, 88]
        }]
    }],
    chart: {
        type: "boxPlot",
        height: 350,
        toolbar: {
            show: !1
        }
    },
    plotOptions: {
        bar: {
            horizontal: !0,
            barHeight: "50%"
        },
        boxPlot: {
            colors: {
                upper: chartBoxPlotHoriColors[0],
                lower: chartBoxPlotHoriColors[1]
            }
        }
    },
    stroke: {
        colors: [chartBoxPlotHoriColors[2]]
    }
}, (chart = new ApexCharts(document.querySelector("#box_plot_hori"), options)).render());