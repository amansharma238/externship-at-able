var remarkdata;
async function func(link,) {
    const response = await fetch(link);
    remarkdata = await response.json();
    remarkdata.forEach(element => {
        console.log(element)
        if (element.lead.id == id && element.user.email == mail) {

            let leadremark = document.getElementById("leadremark")
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
        }
    });
    console.log(remarkdata)
}

var dataTable = document.getElementById('data-table');
var checkItAll = dataTable.querySelector('input[name="select_all"]');
var inputs = dataTable.querySelectorAll('tbody>tr>td>input');

checkItAll.addEventListener('change', function () {
    if (checkItAll.checked) {
        inputs.forEach(function (input) {
            input.checked = true;
        });
    }
});


var dataTable2 = document.getElementById('data-table2');
async function funcName(filter) {
    console.log(filter)
    const response = await fetch("http://127.0.0.1:8000/api/leads/?page=1&state=" + filter);
    var data = await response.json();
    data.results.forEach(lead => {
        // console.log(lead)
        let check = document.createElement('input')
        check.type = "checkbox"
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
        state.innerText = lead.state
        assigned.innerText = lead.user_id.first_name + " " + lead.user_id.last_name
        console.log(lead.user_id.email, lead.id)

        view.innerHTML = "<input type='button' id=" + lead.user_id.email + "/" + lead.id + " value='view' class='button'/>"

        console.log("view: ", view)
        row.append(check, id, name, email, phone_number, assigned, state, view)
        dataTable2.append(row)
    })
}

let filter = ""
function myfunc(e) {
    // console.log(e);
    filter = e.target.value;
    dataTable2.innerHTML = ""
    funcName(filter);
}
const e1 = document.querySelectorAll("#leadsinput");
e1.forEach(i => {
    i.addEventListener("click", myfunc);
})
funcName(filter);



// func("http://127.0.0.1:8000/api/remarks/", lead.user_id.email, lead.id)

// view.addEventListener('click', () => {
//     modal_container.classList.add('show');
// })


// const open = document.getElementById('open');
const modal_container = document.getElementById('modal_container');
const close = document.getElementById('close');

close.addEventListener('click', () => {
    modal_container.classList.remove('show');
})