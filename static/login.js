import { myFetch, eval_status_code } from "./utils.js";

document.addEventListener("DOMContentLoaded", ()=>{

    let token = localStorage.getItem("token");

    if (token && token!="undefined"){
        
        window.location.replace("home");
    }
    else{
        console.log("YOu have to login");
    //login /register form
    let form = document.createElement("form");
    form.setAttribute("action", "/api/token");
    form.setAttribute("method", "post");


    let container = document.createElement("div");
    form.append(container);

    let title_div = document.createElement("div");
    title_div.innerHTML += "Login";

    let name_div = document.createElement("div");
    let name_label = document.createElement("label");
    name_label.innerHTML+= "Name";

    let username = document.createElement("input");
    username.setAttribute("name", "username");
    username.setAttribute("placeholder", "username");
    name_div.append(name_label, username)
        
    let password_div = document.createElement("div");
    let password_label = document.createElement("label");
    password_label.innerHTML+= "Password";

    let password = document.createElement("input");
    password.setAttribute("name", "password");
    password.setAttribute("placeholder", "password");

    password_div.append(password_label, password);

    let submit_div  = document.createElement("div");
    let submit = document.createElement("input");
    submit.setAttribute("type", "submit");
    submit_div.append(submit);

    let to_register_div = document.createElement("div");
    let register = document.createElement("a");
    register.innerHTML += "Register";
    register.setAttribute("href", "");

    //if register clicked change title to register
    //change button event listener
    //to_register_div innerhtml to already have an account login
    //add event listener to login that reverses effect
    register.addEventListener("click", (event)=>{
        event.preventDefault();
        title_div.innerHTML = "Register";

        
    })

    to_register_div.append("Dont have an account yet?", register);

    container.append(title_div, name_div, password_div,submit_div, to_register_div);


    form.addEventListener("submit", async (event)=>{
        event.preventDefault();
        let [response, status_code] = await  myFetch("api/token/", "POST", new FormData(form));

        if (eval_status_code){
            localStorage.setItem("token", response["access"]);
            window.location.replace("home");
        }
    })



    document.body.append(form);}
})