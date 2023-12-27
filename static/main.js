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
        //console.log(result);
    })

    //load home page immediately upon visit
    load_home();

    //clicking anywhere else clears any popup forms
    window.addEventListener("click", ()=>{
        clear_popups();
    })
    
    let divs = document.querySelectorAll(`div`);
    console.log("divs", divs.length);
})
const row_gap = window.getComputedStyle(document.documentElement).getPropertyValue("--row-gap");
const row_gap_float = Number(row_gap.slice(0,-3)) * 16;

//getting needed variables
const row_height = window.getComputedStyle(document.documentElement).getPropertyValue("--row-height");
const row_height_float = Number(row_height.slice(0,-3)) * 16; //convert to pixels by * 16

const DAY_LIST = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]

function load_home(){
    console.log("loading home");
    //initial calendar load when user logs in
    //get last viewed calendar id, that is the calendar that will be loaded on browser load
    fetch("api/LastViewedCalendar/",{
    headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
    }})
    .then(res => res.json())
    .then(result => {
        let last_viewed = result["id"];
        
        //load a calendar
        load_calendar(last_viewed); 


        //settin up sidebar- getting all user calendars and displaying them----------------------------------
        fetch("api/ScheduleCalendars/",{
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        })
        .then(res => res.json())
        .then(result => {
            //console.log(result);

            let sidebar = document.querySelector("#sidebar");

            //putting calendars into sidebar ------------------------------------------
            result.forEach((calendar) =>{
                let cal_container = document.createElement("div");
                sidebar.append(cal_container);
                cal_container.classList.add("sidebar-item");
                cal_container.innerHTML += calendar.name;

                if (calendar.id == last_viewed){
                    cal_container.style.backgroundColor = "grey";
                }
                
                //adding event listener so when calendar is clicked it loads calendar --------------------------
                cal_container.addEventListener("click", ()=>{
                    //change last viewed calendar to clicked one then reload
                    fetch("api/LastViewedCalendar/", {
                        method :"PUT",
                        headers:{
                            Authorization: `Bearer ${localStorage.getItem("token")}`,
                            "Content-Type": "application/json"
                        },
                        body:JSON.stringify({"id": calendar.id})
                        
                    })
                    .then(res => res.json())
                    .then(result => {
                        //clear places that need to be cleared 
                        clear_screen();
                        load_home();
                    })
                })
            })
        })
        })
}

function load_calendar(cal_id){
    fetch( `api/ScheduleCalendars/${cal_id}`,{
        headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`
        }
    })
    .then(res => res.json())
    .then(result => {

    //grid that holds calendar
    let calendar_grid = document.querySelector("#calendar-grid");
    calendar_grid.setAttribute("id", "calendar-grid");

    //LABEL COLUMN OF CALENDAR --------------------------------------------
    let first_column = document.querySelector("#label-col");

    first_column.classList.add("label-col");
    let label = document.createElement("div");
    first_column.append(label);
        
    label.classList.add("schedule-name");
    label.innerHTML += "GMT +00";
    

    let label_col = document.createElement("div");
    first_column.append(label_col);
    label_col.classList.add("label-items");

    for(let i=1; i<25; i++){
        let label = document.createElement("div");
    
        label.classList.add("label");
        if (i <= 11){
            label.innerHTML += `${i} AM`;

        }else{
            label.innerHTML += `${i} PM`;

        }
        label_col.append(label)
        }
     //  end of label column -----------------------------------------------------------------
    

    //LOADING SCHEDULES --------------------------------------------------------------
    let name = ""; 
        let schedules = result["schedules"];
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
    let name = schedule["name"];
    fetch(`api/Schedule/${schedule["id"]}`, {
        headers:{
            Authorization:`Bearer ${localStorage.getItem("token")}`
        }
        })
    .then( res => res.json())
    .then(schedule => {
        //console.log(schedule);
        //main part of calendar --------------------------------------------------------------
        let schedule_column = document.querySelector(`#schedule${Number(name)}`);
        schedule_column.classList.add("schedule-col");

        //title's of columns----------------------------------------
        let title_container = document.createElement("div");
        schedule_column.append(title_container);
        title_container.classList.add("schedule-name");

        title_container.innerHTML += schedule["name"].substr(0, 3).toUpperCase();
        // end of title

        // event column
        let event_column = document.createElement("div");
        schedule_column.append(event_column);
        event_column.classList.add("event-col");

        //event boxes ----------------------------------------------------
        for (let i=0; i<24; i++){
            let event_box = document.createElement("div");
            event_column.append(event_box);

            event_box.setAttribute("data-schedule", `${schedule["id"]}`);
            event_box.setAttribute("data-event", `${i}`);

            event_box.classList.add("event-box");

            // event listener---------------------------------------------------------
            // click on box triggers procedure to add an event
            event_box.addEventListener("click", (event) => clickbox(event, Number(name), i, "box"))
     
        }

        
        let events = schedule["events"];

        //placing events on grid ----------------------------------------------------------------------
        events.forEach((event_object, index) =>{
            let [start_hour, start_minute, time_difference, hour_difference, gap_number,end_hour, end_minute ] = parse_time(event_object);
            
            let to_place = document.querySelector(`div[data-event="${start_hour}"][data-schedule="${schedule["id"]}"]`);

            // container of event
            let event_container = document.createElement("div");
            event_container.setAttribute("data-eventid", event_object["id"]);
            
            // setting height of event container based on how long event is
  
            // height = row_height * time_difference + row_gap * gap_number;
            //rowheight * timedifference - makes sure height of event is proportional to time it take,
            //row_gap blah blah blah takes into account gaps in grid
            event_container.style.height= `${row_height_float* time_difference + row_gap_float* gap_number}px`;
        
            event_container.classList.add("event-container");

           
            /* We want event boxes to line up nicely. however using absolute positioning everywhere brings out the inaccuracies using calculations
            We then want to use position relative if event has a prior one so that it is placed immediately after prior event,
            however events without prior events or those with prior events that are absolutely positioned will fall to the top, 
            means we want to conditionally render  */

            /* if event has immediate prior event that starts in the same box or start minute = 0 use position relative and no offset
            else add an offset to top*/

            let offset = (row_height_float * start_minute / 60);
            event_container.style.top = `${offset}px` ;

            to_place.append(event_container);
            
            //adding eventlistener to events
            //such that when events are clicked form pops up immediately to their side and form is prepopulated
            event_container.addEventListener("click", (event) => clickbox(event, Number(name), start_hour,  "event",offset,event_object["id"]))


            // title of event
            let title_container = document.createElement("div");
            event_container.append(title_container);
            title_container.classList.add("event-title");
            title_container.innerHTML += `${event_object["title"]}`;

            // time of event
            //add if event length is 15 min or greatere

            if (time_difference >= 0.25){
            let time_container = document.createElement("div");
            event_container.append(time_container);
            time_container.classList.add("event-time");
            time_container.innerHTML += `${event_object["start_time"]}-${event_object["end_time"]}`;
            }
        }) 
        
    })
}
        
function clickbox(event , schedule_number, box_number, box_or_event, offset, event_details ){
    /* caters to both clicking an empty box or clicking an event
    box_or_container - differentiates whether box or event */
    event.stopPropagation();
    //clear other popups on screen
    clear_popups();
    // use schedule number and box number to locate box which was clicked  
    let event_box = document.querySelector(`#schedule${schedule_number} div[data-event="${box_number}"]`);
    console.log("event ob", event_box);

    // popup form to submit ------------------------------------------------------
    let form = document.createElement("form");
    event_box.append(form);
    
    if (box_or_event == "event"){
        form.style.top = `${offset}px`;
    }

    form.classList.add("popup-form","animate");

    form.setAttribute("action", `/`)
    //form.setAttribute("method", "post");

  
    // if x coordinate is more than half the screen width popup to left of box instead of to right of box 
    let x = event.clientX;
    let half_screen_size = window.innerWidth/2;

    if (x > half_screen_size){
        form.style.left = "-233%";
        form.classList.add("slideInRight");
    }else{
        form.classList.add("slideInLeft");
    }

    // form container -----------------------------------------------------
    let form_container = document.createElement("div");
    
    form.append(form_container)
    form_container.classList.add("popup-form-container");

    let title_input = document.createElement("input");
    form_container.append(title_input);
    //add form to box
    title_input.focus();


    form.addEventListener("click", (e)=>{
        //stop other click events happening when workin on the form
        e.stopPropagation();

        // let current = document.querySelector(`#schedule3 div[data-event="22"]`);
        // console.log("current", current);
        // current.scrollIntoView({ behavior: "smooth"});
      
    })
    
    //form.style.display = "block";
   
}



function clear_screen(){
    // clear screen mainly for calendar switching

    //clear sidebar
    document.querySelector("#sidebar").innerHTML = "";
    //clear grid
    document.querySelector(".label-col").innerHTML =  "";

    document.querySelectorAll(".schedule-col").forEach(column => column.innerHTML = "");

}

function clear_popups(){
    // clicking anywhere removes popup forms
    let popups = document.querySelectorAll(".popup-form");
    popups.forEach((form)=>{
        form.classList.add("disappear");
        form.style.display = "none";
    }) 
}

function parse_time(event){
    // parsing event start and end times
    let start_time = event["start_time"];
    let end_time = event["end_time"];

    let start_hour = Number(start_time.substr(0,2));
    let end_hour = Number(end_time.substr(0,2));
    
    let start_minute = Number(start_time.substr(3,2));
    let end_minute = Number(end_time.substr(3,2));

    let time_difference = (end_hour + end_minute/60 )- (start_hour +  start_minute/60);
    let hour_difference = end_hour - start_hour;

    let crossover;

    if (end_minute != 0){
        crossover = 1;
    }else{
        crossover = 0;
    }

    let gap_number = hour_difference - 1 + crossover;

    return [start_hour, start_minute, time_difference, hour_difference, gap_number, end_hour, end_minute];
}

