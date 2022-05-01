function load_params(name, processes){
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