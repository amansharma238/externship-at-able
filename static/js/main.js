// greeting

const user_email = JSON.parse(document.getElementById('user_id').textContent);
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

// check all checkboxes
function checkBoxToggle(source) {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i] != source)
            checkboxes[i].checked = source.checked;
    }
}

async function changeStatus(rawdata) {
    var token = getCookie('csrftoken');
    fetch(`/api/leads/${rawdata.id}`, {
        method: 'PUT',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'X-CSRFToken': token
        },
        body: JSON.stringify(rawdata),
    }).then(res => res.json())
        .then(res => console.log(res));

}

// Implement filters
var plink = "/api/leads/?page=1"
let filter = ""
function myfunc(e) {
    filter = e.target.value;
    filterFunction(plink, filter);
}
const e1 = document.querySelectorAll("#leadsinput");
e1.forEach(i => {
    i.addEventListener("click", myfunc);
})
filterFunction(plink, filter);

async function filterFunction(link, filter) {
    var dataTable2 = document.getElementById('data-table2');
    let response;
    if (filter === "") {
        response = await fetch(link);
    }
    else
        response = await fetch(link + "&state=" + filter);
    dataTable2.innerHTML = ""
    var data = await response.json();
    // console.log(data.results)
    data.results.forEach(lead => {
        let check = document.createElement('input')
        check.type = "checkbox"
        let check_box = document.createElement('td');
        check_box.append(check);
        let row = document.createElement('tr')
        let name = document.createElement('td')
        let email = document.createElement('td')
        let phone_number = document.createElement('td')
        let state = document.createElement('td')
        let assigned = document.createElement('td')
        let id = document.createElement('td')
        let view = document.createElement('td')
        id.innerText = lead.id
        name.innerText = lead.name
        email.innerText = lead.email
        phone_number.innerText = lead.phone_number
        let anArray = ["New Lead", "Hot Lead", "Med Lead", "Grey Lead", "Success"];
        let new_list = anArray.splice(anArray.indexOf(lead.state), 1);
        state.innerHTML = "<select name='states' id='state' class='nlead " + (lead.state).replace(/\s+/g, '') + "'>\
                        <option class='nlead "+ (lead.state).replace(/\s+/g, '') + "' value='" + lead.state + "'>" + lead.state + "</option>\
                        <option class='nlead "+ anArray[0].replace(/\s+/g, '') + "' value='" + anArray[0] + "'>" + anArray[0] + "</option>\
                        <option class='nlead "+ anArray[1].replace(/\s+/g, '') + "' value='" + anArray[1] + "'>" + anArray[1] + "</option>\
                        <option class='nlead "+ anArray[2].replace(/\s+/g, '') + "' value='" + anArray[2] + "'>" + anArray[2] + "</option>\
                        <option class='nlead "+ anArray[3].replace(/\s+/g, '') + "' value='" + anArray[3] + "'>" + anArray[3] + "</option>\
                        </select>"
        state.querySelector("select").addEventListener('change', (e) => {
            // console.log(e.target.value);
            var new_data = lead;
            new_data.state = e.target.value;
            // console.log("new data: ", new_data);
            changeStatus(new_data);
        });
        assigned.innerText = lead.user_id.first_name + " " + lead.user_id.last_name

        // console.log(lead.user_id.email, lead.id)

        view.innerHTML = "<input type='button' id=" + lead.user_id.email + "/" + lead.id + " value='view' class='button' onmouseover='zoom(this);' />"
        // console.log("valueeeeee: ", view.children[0].value);

        if (user_email !== lead.user_id.email) {
            state.lastChild.disabled = true;
            view.lastChild.disabled = true;
        }

        let viewvar = remarkFunc("/api/remarks/" + lead.user_id.email + "/" + lead.id)
        // console.log("dkjsdkj ", viewvar);

        view.addEventListener('click', (e) => {
            remarkFunc("/api/remarks/" + lead.user_id.email + "/" + lead.id)
            modal_container.classList.add('show');
        })
        row.append(check_box, id, name, email, phone_number, assigned, state, view)
        dataTable2.append(row)
    })
}


function getCookie(name) {
    var v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return v ? v[2] : null;
}


// Implement remarks

let rawdata = {}
async function zoom(ele) {
    var id = ele.id;
    var iid = id.split('/')[1];
    // console.log("iiidd ", parseInt(iid));
    const response = await fetch("/api/remarks/" + id);
    remarkdata = await response.json();
    rawdata = {
        "remark": '',
        "lead": iid,
    }
}

function passData($this) {
    var val = $this.previousElementSibling.value;
    // console.log("value   ", val);
    if (val == '') {
        console.log('no input');
    } else {
        rawdata["remark"] = val;
    }
    let form = document.getElementById("userremark")
    let pp = form.querySelector("input[name='csrfmiddlewaretoken']");
    rawdata.csrfmiddlewaretoken = pp.value;

    console.log("rawdata:   ", rawdata)
    if (rawdata != {} && rawdata["remark"] != '') {
        fetch('/api/remarks/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
                'X-CSRFToken': pp.value
            },
            body: JSON.stringify(rawdata),
        }).then(res => res.json())
            .then(res => console.log(res));
    }
}

var remarkdata;
async function remarkFunc(link) {
    const response = await fetch(link);
    remarkdata = await response.json();
    // console.log("rrrr ", remarkdata);
    let leadremark = document.getElementById("leadremark")
    leadremark.innerHTML = ""
    remarkdata.forEach(element => {
        let user = document.createElement("h5")
        user.innerText = element.user.first_name + " " + element.user.last_name
        let created = document.createElement("p")
        let date = new Date(element.created);
        const formattedDate = date.toLocaleString("en-US", {
            day: "numeric",
            month: "short",
            year: "numeric",
            hour: "numeric",
            minute: "2-digit"
        });
        created.innerText = formattedDate
        let remark = document.createElement("p")
        remark.innerText = element.remark
        leadremark.append(user, created, remark)
    });
}

// pagination
function paginateFunc(link) {
    filterFunction(link, filter);
    Pagination(link)
    if (link == "/api/leads/")
        plink = link + "?page=1"
}

async function Pagination(link) {
    const response = await fetch(link);
    var data = await response.json();
    var paginate = document.getElementById('paginator');
    paginate.innerHTML = ""
    if (data.previous != null) {
        var pre = document.createElement('input')
        pre.setAttribute('value', 'previous')
        pre.setAttribute('type', 'button')
        paginate.append(pre)
        pre.addEventListener('click', () => paginateFunc(data.previous));
    }
    if (data.next != null) {
        var next = document.createElement('input')
        next.setAttribute('value', 'next')
        next.setAttribute('type', 'button')
        paginate.append(next)
        next.addEventListener('click', () => paginateFunc(data.next));
    }
}

Pagination(plink)

// const open = document.getElementById('open');
const modal_container = document.getElementById('modal_container');
const close = document.getElementById('close');

close.addEventListener('click', () => {
    modal_container.classList.remove('show');
})