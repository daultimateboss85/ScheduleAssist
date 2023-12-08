document.addEventListener("DOMContentLoaded", ()=>{
    //going to make this such that on login get user token
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

    //load home page immediately after displaying last viewed calendar or default calendar if none
    load_home();
})

const DAY_LIST = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]

function load_home(){
    //initial calendar load when user logs in
    //somehow get last viewed calendar id
    let last_viewed = 7;

    //set up sidebar and top bar


    //load a calendar
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

    //grid that holds calendar
    let calendar_grid = document.querySelector("#calendar-grid");
    calendar_grid.setAttribute("id", "calendar-grid");

    //LABEL COLUMN OF CALENDAR --------------------------------------------
    let first_column = document.querySelector("#label-col");

    first_column.classList.add("label-col");

    for(let i=0; i<25; i++){
        let label = document.createElement("div");
        label.classList.add("label");
        if (i == 0){
            // label.classList.add("schedule-name");
            label.innerHTML += "GMT +00";
        }else{
            if (i <= 11){
                label.innerHTML += `${i} AM`;

            }else{
                label.innerHTML += `${i} PM`;

            }
        }
        first_column.append(label);
    } //  end of label column -----------------------------------------------------------------
    

    //LOADING SCHEDULES --------------------------------------------------------------
    let name = ""; 
        const schedules = result["schedules"];
        for(let i = 0; i < schedules.length; i++){
            //iterate through schedules picking only main schedule 
            let schedule = schedules[i];
            if (schedule["name"] != name && schedule["name"] != "0"){
                name = schedule["name"];

                load_schedule(schedule);
            } 
        }
    })
}


function load_schedule(schedule){
    const name = schedule["name"];
    fetch(`api/Schedule/${schedule["id"]}`, {
        headers:{
            Authorization:`Bearer ${localStorage.getItem("token")}`
        }
        })
    .then( res => res.json())
    .then(schedule => {
        console.log(schedule);
        
        //main part of calendar --------------------------------------------------------------
        let schedule_column = document.querySelector(`#schedule${Number(name)}`);

        schedule_column.classList.add("schedule-col");

        //title's of columns
        let title_container = document.createElement("div");
        schedule_column.append(title_container);
        title_container.classList.add("schedule-name");

        title_container.innerHTML += schedule["name"].substr(0, 3).toUpperCase();
        // end of title

        //event boxes
        for (let i=0; i<24; i++){
            let event_box = document.createElement("div");
            schedule_column.append(event_box);

            event_box.setAttribute("data-schedule", `schedule${schedule["id"]}`);
            event_box.setAttribute("data-event", `${i}`);

            event_box.classList.add("cal-event");
        }


        const events = schedule["events"];

        events.forEach((event_object, index) =>{
        
            let start = Number(event_object["start_time"].substr(0,2));
            console.log(start);
          
            let to_place = document.querySelector(`div[data-event="${start}"]`);

            let event = document.createElement("div");
            event.innerHTML += `${event_object["title"]}`;
            to_place.append(event);
        }) 
        
    })
}
        //title of column

  
        
        /*     for(let j=0; j<24; j++){
                
        
                if(j==0){
                    cal_box.classList.add("schedule-name");
                    cal_box.innerHTML += DAY_LIST[i];
                }else{

                    cal_box.classList.add("cal-event");
                    cal_box.innerHTML += "Some event\n" + "12:00 - 15:00";
                }
            }
         */

/*         }
    })

    

} */