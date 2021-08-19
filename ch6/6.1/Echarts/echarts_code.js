var uploadedDataURL = "/asset/get/s/data-1572510841921-XM77Rmhs.json";
$.getJSON(uploadedDataURL, function(linedata) {
    var data = linedata[0];
    var links = linedata[1];
    var categories = linedata[2];
    data.forEach(function(data) {
        data.itemStyle = null;
        data.label = {
            normal: {
                show: data.symbolSize > 15
            }
        };
    });
    option = {
        title: {
            text: "人物公司关系",
            top: "top",
            left: "left"
        },
        tooltip: {},
        toolbox: {
            show: true,
            feature: {
                dataView: {
                    show: true,
                    readOnly: true
                },
                restore: {
                    show: true
                },
                saveAsImage: {
                    show: true
                }
            }
        },
        animationDuration: 1500,
        animationEasingUpdate: 'quinticInOut',
        legend: [{
            data: categories.map(function(a) {
                return a.name;
            })
        }],
        series: [{
            name: '人物公司关系',
            type: 'graph',
            layout: 'force',
            force: {
                //initLayout:'circular'
                edgeLength: 120,
                repulsion: 100,
                gravity: 0.2
            },
            data: data,
            links: links,
            categories: categories,
            focusNodeAdjacency: true,
            roam: true,
            label: {
                normal: {
                    position: 'right',
                    formatter: '{b}'
                }
            },
            lineStyle: {
                color: 'source',
                curveness: 0.3
            },
            itemStyle: {
                normal: {
                    borderColor: '#fff',
                    borderWidth: 1,
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.3)'
                }
            },
            emphasis: {
                lineStyle: {
                    width: 10
                }
            }
        }]
    };
    myChart.setOption(option)
})