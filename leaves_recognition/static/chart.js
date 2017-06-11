var ctx = document.getElementById("myDoughnutChart");
                var data = {
                    labels: [
                        "{{first_label}}",
                        "{{second_label}}"
                    ],
                    datasets: [
                        {
                            data: [100, 100],
                            backgroundColor: [
                                "#FF6384",
                                "#36A2EB"
                            ],
                            hoverBackgroundColor: [
                                "#FF6384",
                                "#36A2EB"
                            ]
                        }]
                };
                    var myDoughnutChart = new Chart(ctx, {
                        type: 'doughnut',
                        data: data,
                        options: {
                            responsive: false
                        }
                    });