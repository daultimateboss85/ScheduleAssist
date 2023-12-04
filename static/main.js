document.addEventListener("DOMContentLoaded", ()=>{

    fetch("api/token/", {
        method: "POST",
        headers:{
            "Content-Type": "application/json"},

        body: JSON.stringify({"username": "judah", "password":"thechosenone"})
    })
    .then(res => res.json())
    .then(result => {
        localStorage.setItem("token", result["access"])
        console.log(result)
    })

    load_home();
})

const DAY_LIST = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]

function load_home(){
    //initial calendar load when user logs in
    console.log("hello")

    //somehow get last viewed calendar id
    let last_viewed = 2;

    load_calendar(last_viewed);
}


function load_calendar(cal_id){
    fetch( `api/ScheduleCalendars/${cal_id}`,{
        headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`
        }
    })
    .then(res => res.json())
    .then(result => {

    console.log(result);
    //section of screen that holds calendar grid
    let main_grid = document.querySelector("#maingrid");

    //grid that holds calendar
    let calendar_grid = document.createElement("div");
    calendar_grid.setAttribute("id", "calendar-grid");

    //label column of calendar --------------------------------------------
    let first_column = document.createElement("div");
    calendar_grid.append(first_column);

    first_column.classList.add("label-col");

    let name = ""; 
    const schedules = result["schedules"];
    for(let i = 0; i < schedules.length; i++){
        let schedule = schedules[i];
        if (schedule["name"] != name){
            name = schedule["name"]
            load_schedule(schedule["id"]);
        } 
    }


    for(let i=0; i<24; i++){
        let label = document.createElement("div");
        label.classList.add("label");

        if (i == 0){
            label.innerHTML += "GMT +00";
        }else{
            if (i <= 11){
                label.innerHTML += `${i} AM`;
            }else{
                label.innerHTML += `${i} PM`;

            }
        
        }

        first_column.append(label);
    }
    
    //main part of calendar --------------------------------------------------------------
    for (let i=0; i<7; i++){
        let schedule_column = document.createElement("div");
        calendar_grid.append(schedule_column);
        schedule_column.classList.add("schedule-col");


        for(let j=0; j<24; j++){
            let cal_box = document.createElement("div");
            schedule_column.append(cal_box);


            if(j==0){
                cal_box.classList.add("schedule-name");
                cal_box.innerHTML += DAY_LIST[i];
            }else{

                cal_box.classList.add("cal-event");
                cal_box.innerHTML += "Some event\n" + "12:00 - 15:00";
            }
        }
        

    }

    main_grid.append(calendar_grid);
    
    })
}

function load_schedule(schedule_id){

}