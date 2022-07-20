var myDate = new Date();
var hrs = myDate.getHours();
var greet;
if (hrs < 12)
    greet = 'Good Morning';
else if (hrs >= 12 && hrs <= 17)
    greet = 'Good Afternoon';
else if (hrs >= 17 && hrs <= 24)
    greet = 'Good Evening';
document.getElementById("greet").innerText = document.getElementById("greet").innerText.replace("Good Morning", greet)

function lead_sum(s, newdata) {
    var sum = 0;
    newdata.forEach(e => {
        if (e.state === s)
            sum++;
    });
    return sum;
}

var data;
async function funcName(link) {
    newdata = []
    while (true) {
        const response = await fetch(link);
        data = await response.json();
        data.results.forEach(i => {
            newdata.push(i)
        })
        if (data.next == null)
            break;
        link = data.next
    }
    return newdata
}

async function dataFunc() {
    newdata = await funcName("/api/leads/");
    let arr = [];
    let rank = {};
    let rrank = {};
    newdata.forEach(lead => {
        let date = new Date(lead.created);
        date = date.getDate() + "/" + (date.getMonth() + 1)
        arr.push(date)
        if (lead.user_id.email in rank && lead.state == 'Hot Lead') {
            rank[lead.user_id.email] += 1
            rrank[lead.user_id.first_name + " " + lead.user_id.last_name] += 1
        }
        else if (lead.state == 'Hot Lead') {
            rank[lead.user_id.email] = 1
            rrank[lead.user_id.first_name + " " + lead.user_id.last_name] = 1
        }

    })

    const sorted = Object.entries(rrank)
        .sort(([, v1], [, v2]) => v2 - v1)
        .reduce((obj, [k, v]) => ({
            ...obj,
            [k]: v
        }), {})

    var index = 1;
    for (i in sorted) {
        let sales = document.getElementById("analytics-body");
        let row = document.createElement('tr');
        let name = document.createElement('td');
        let leadconverted = document.createElement('td');
        let ind = document.createElement('td');
        name.innerText = i;
        leadconverted.innerText = sorted[i];
        ind.innerHTML = `#${index}`;
        row.append(ind, name, leadconverted);
        sales.append(row);
        index += 1;
    }

    let obj = {}
    Date.prototype.addDays = function (days) {
        this.setDate(this.getDate() + parseInt(days));
        return this;
    };

    for (var i = 36; i >= 0; i--) {
        let newDate = new Date().addDays(-i);
        obj[newDate.getDate() + "/" + (newDate.getMonth() + 1)] = [{}];
    }
    let j = 0;
    arr.forEach(i => {
        if (i in obj) {
            obj[i].push(newdata[j])
        }
        j += 1;
    })

    var res = {};
    let x = Object.keys(obj).length;
    var dateselect = "Last 7 days";
    var myChart = null;

    function changefunc(dateselect) {
        res = {};
        if (dateselect == "Last 7 days") {
            let newobj = Object.entries(obj).slice(x - 7, x)

            for (pair of newobj) {
                const [key, value] = pair;
                res[key] = value;
            };
        }
        else if (dateselect == "Last Week") {
            let newobj = Object.entries(obj).slice(x - 14, x - 7)

            for (pair of newobj) {
                const [key, value] = pair;
                res[key] = value;
            };
        }
        else if (dateselect == "Last Month") {
            let newobj = Object.entries(obj).slice(x - 37, x - 30)

            for (pair of newobj) {
                const [key, value] = pair;
                res[key] = value;
            };
        }

        // console.log("ress", res);
        hot = {}
        med = {}
        grey = {}


        newhot = {}
        newmed = {}
        newgrey = {}

        for (let i in obj) {
            if (!(i in hot))
                hot[i] = 0
            obj[i].forEach(j => {
                if (j.state === "Hot Lead")
                    hot[i] += 1
            })
        }

        for (let i in obj) {
            if (!(i in med))
                med[i] = 0
            obj[i].forEach(j => {
                if (j.state === "Med Lead")
                    med[i] += 1
            })
        }

        for (let i in obj) {
            if (!(i in grey))
                grey[i] = 0
            obj[i].forEach(j => {
                if (j.state === "Grey Lead")
                    grey[i] += 1
            })
        }

        for (let i in res) {
            if (!(i in newhot))
                newhot[i] = 0
            res[i].forEach(j => {
                if (j.state === "Hot Lead")
                    newhot[i] += 1
            })
        }

        for (let i in res) {
            if (!(i in newmed))
                newmed[i] = 0
            res[i].forEach(j => {
                if (j.state === "Med Lead")
                    newmed[i] += 1
            })
        }

        for (let i in res) {
            if (!(i in newgrey))
                newgrey[i] = 0
            res[i].forEach(j => {
                if (j.state === "Grey Lead")
                    newgrey[i] += 1
            })
        }

        var totalhot = lead_sum("Hot Lead", newdata);
        var totalmed = lead_sum("Med Lead", newdata);
        var totalgrey = lead_sum("Grey Lead", newdata);
        var total = newdata.length;

        let totaldiv = document.getElementById("ttotal");
        totaldiv.innerHTML = `<h2>${total}</h2>`;

        let hotdiv = document.getElementById("hhot");
        hotdiv.innerHTML = `<h2>${totalhot}</h2>`;

        let meddiv = document.getElementById("mmed");
        meddiv.innerHTML = `<h2>${totalmed}</h2>`;

        let grediv = document.getElementById("ggre");
        grediv.innerHTML = `<h2>${totalgrey}</h2>`;

        let data_list = [
            {
                label: 'Hot',
                backgroundColor: "#caf270",
                data: Object.values(newhot),
            },
            {
                label: 'Med',
                backgroundColor: "#45c490",
                data: Object.values(newmed),
            },
            {
                label: 'Grey',
                backgroundColor: "#008d93",
                data: Object.values(newgrey),
            }
        ]

        var ctx = document.getElementById("myChart4").getContext('2d');
        if (myChart != null)
            myChart.destroy();

        myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(res),
                datasets: data_list,
            },
            options: {
                tooltips: {
                    displayColors: true,
                    callbacks: {
                        mode: 'x',
                    },
                },
                plugins: {
                    datalabels: {
                        display: true,
                        align: 'center',
                        anchor: 'center'
                    }
                },
                scales: {
                    xAxes: [{
                        stacked: false,
                        gridLines: {
                            display: false,
                        }
                    }],
                    yAxes: [{
                        stacked: true,
                        ticks: {
                            beginAtZero: true,
                        },
                        type: 'linear',
                    }]
                },
                responsive: true,
                maintainAspectRatio: false,
                legend: { position: 'bottom' },
            }
        });
    }
    changefunc(dateselect)
    function changedays(e) {
        changefunc(e.target.value);
    }
    let day = document.getElementById("select-days");
    day.querySelector("select").addEventListener('change', changedays);
}
dataFunc();