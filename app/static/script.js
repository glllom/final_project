function change_product(id, name, processes){
    let form = document.querySelector("#change_form");
    form.action = "/change_product/" + id;
    let form_name = document.querySelector("#change_form_name");
    let form_processes = document.querySelectorAll("#change_form_processes>option");
    form_name.value = name;
    for (let i=0; i<form_processes.length; i++){
        form_processes[i].removeAttribute("selected");
    }
    for (num of processes){
        form_processes[num-1].setAttribute("selected", true);
    }
}

function change_process(id, name, employee, products){
    let form = document.querySelector("#change_form");
    form.action = "/change_process/" + id;
    let form_name = document.querySelector("#change_form_name");
    let form_employee = document.querySelector("#change_form_employee");
    let form_products = document.querySelectorAll("#change_form_products>option");
    form_name.value = name;
    form_employee.value =  employee;
    for (let i=0; i<form_products.length; i++){
        form_products[i].removeAttribute("selected");
    }
    for (num of products){
        form_products[num-1].setAttribute("selected", true);
    }
}