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
        console.log(result);
    })

    //load home page immediately upon visit
    load_home();

    //clicking anywhere else clears any popup forms
    window.addEventListener("click", ()=>{
        clear_popups();
    })
    
})
const row_gap = window.getComputedStyle(document.documentElement).getPropertyValue("--row-gap");
const row_gap_float = Number(row_gap.slice(0,-3)) * 16;

//getting needed variables
const row_height = window.getComputedStyle(document.documentElement).getPropertyValue("--row-height");
const row_height_float = Number(row_height.slice(0,-3)) * 16; //convert to pixels by * 16

const DAY_LIST = [ "MASTER", "MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

//work around javascript days starting on Sunday
const DAY_CONVERSION = {0:"7", 1:"1", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6"}

function load_home(){
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
         
            let sidebar = document.querySelector("#sidebar");
            let cal_title = document.createElement("div");
            sidebar.append(cal_title)

            let addcalendar = document.createElement("span");
            addcalendar.innerHTML += " +";

            cal_title.classList.add("title");
            cal_title.append("Calendars" ,addcalendar);
            
            let cal_container = document.createElement("div");
            sidebar.append(cal_container);
            cal_container.classList.add("cal-container")
            

            //add calendar -----------------------------------------------------
            addcalendar.addEventListener("click", (event) =>{
              
                event.stopPropagation();
                clear_popups();
                let form = document.createElement("form");
                let container = document.createElement("div");
                form.append(container);
                container.classList.add("sidebar-item", "new-form");
                
                let cal_name = document.createElement("input");
                cal_name.setAttribute("placeholder", "Calendar name");
                cal_name.setAttribute("name", "name");
                container.append(cal_name);
                cal_container.append(form);
                cal_name.focus();

                form.addEventListener("submit", async (event)=>{
                    event.preventDefault();
                    let [response, status_code] = await myFetch("api/ScheduleCalendars/", "POST", body= new FormData(form));
                    
                    if (status_code==201){
                        myFetch("api/LastViewedCalendar/", "PUT", 
                        body=JSON.stringify({"id": response["object"]["id"]}),"application/json");
                        clear_screen();
                        load_home();
                        flash_message(response["message"], status_code);

                    }
                })
                
            })
            //putting calendars into sidebar ------------------------------------------
            result.forEach((calendar) =>{
                let cal_item = document.createElement("div");
                cal_container.append(cal_item);
                
                cal_item.classList.add("sidebar-item");
                
                let button_div = document.createElement("div");
                
                let edit = document.createElement("span");
                edit.innerHTML = "edit";
                edit.classList.add("material-symbols-outlined");
            
                
                let delete_button = document.createElement("span");
                delete_button.innerHTML = "delete";
                delete_button.classList.add("material-symbols-outlined");
            
                
                button_div.append(edit, delete_button);
                
                
                cal_item.append( calendar.name, button_div);

                if (calendar["id"] == last_viewed){
                    cal_item.style.backgroundColor = "lightgrey";
                }
                
                //adding event listener so when calendar is clicked it loads calendar --------------------------
                cal_item.addEventListener("click", ()=>{
                    //change last viewed calendar to clicked one then reload
                    fetch("api/LastViewedCalendar/", {
                        method :"PUT",
                        headers:{
                            Authorization: `Bearer ${localStorage.getItem("token")}`,
                            "Content-Type": "application/json"
                        },
                        body:JSON.stringify({"id": calendar["id"]})
                        
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
        
    label.classList.add("gmt");

    label.innerHTML += "GMT +00";
    label.setAttribute("data-hour", 0)

    let label_col = document.createElement("div");
    first_column.append(label_col);
    label_col.classList.add("label-items");

    for(let i=1; i<25; i++){
        let label = document.createElement("div");
        label.setAttribute("data-hour", i)

        label.classList.add("label");
        if (i <= 11){
            label.innerHTML += `${i} AM`;

        }else{
            if(i== 24){
                label.innerHTML = "";
            }else{
                label.innerHTML += `${i} PM`;
            }
        }

        label_col.append(label)
        }
     //  end of label column -----------------------------------------------------------------
    
    //scroll to current time
    /* scroll to label whose hour is current hour */
    let date = new Date()
    let hour = date.getHours();
    
    let to_scroll_to = document.querySelector(`div[data-hour="${hour}"]`)
    to_scroll_to.scrollIntoView();
             
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
    clear_popups();
    let name = schedule["name"];
    let date = new Date;
    let hour = date.getHours();
    let weekday = DAY_CONVERSION[date.getDay()];
    console.log("weekday", weekday);
    fetch(`api/Schedule/${schedule["id"]}`, {
        headers:{
            Authorization:`Bearer ${localStorage.getItem("token")}`
        }
        })
    .then( res => res.json())
    .then(schedule => {
        
        //main part of calendar --------------------------------------------------------------
        let schedule_column = document.querySelector(`#schedule${Number(name)}`);
        
        //clear column
        schedule_column.innerHTML = "";

        schedule_column.classList.add("schedule-col");

        //title's of columns----------------------------------------
        let title_container = document.createElement("div");
        schedule_column.append(title_container);
        title_container.classList.add("schedule-name");
        title_container.setAttribute("data-schedtitle", schedule["id"]);
        title_container.innerHTML += DAY_LIST[Number(schedule["name"])];

        title_container.addEventListener("click", (event) => display_schedule_options(event,schedule) );
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
            event_box.addEventListener("click", (event) => clickbox(event, schedule["id"], i, "box"))

            //adding red line at current time
            if (name == weekday && i == hour){ //if schedule is today 
                let red_line = document.createElement("div");
                red_line.classList.add("red-line");
                let offset = row_height_float * date.getMinutes() / 60;
                red_line.style.top = `${offset}px`;
                event_box.append(red_line);
            }
        }

        let events = schedule["events"];
        
        //placing events on grid ----------------------------------------------------------------------
        events.forEach((event_object, index) =>{
            let [start_hour, start_minute, time_difference, hour_difference, gap_number,end_hour, end_minute ] = parse_time(event_object);
            
            //where ill place event container
            let to_place = document.querySelector(`div[data-event="${start_hour}"][data-schedule="${schedule["id"]}"]`);

            // container of event
            let event_container = document.createElement("div");
            event_container.setAttribute("data-eventid", event_object["id"]);
            
            // setting height of event container based on how long event is
            // height = row_height * time_difference + row_gap * gap_number;
            //rowheight * timedifference - makes sure height of event is proportional to time it takes,
            //row_gap blah blah blah takes into account gaps in grid
            event_container.classList.add("event-container");
            event_container.style.height= `${row_height_float* time_difference + row_gap_float* gap_number}px`;

            /* Just absolutely position all events ha! */
            let offset = (row_height_float * start_minute / 60); //offset to event
            event_container.style.top = `${offset}px` ;

            to_place.append(event_container);
            
            //adding eventlistener to events
            //such that when events are clicked form pops up immediately to their side and form is prepopulated
            event_container.addEventListener("click", (event) => clickbox(event, schedule["id"], start_hour,  "event",offset, event_object))

            // title of event
            let title_container = document.createElement("div");
            event_container.append(title_container);
            title_container.classList.add("event-title");
            title_container.innerHTML += `${event_object["title"]}`;

            // time of event
            //add if event length is 15 min or greater
            if (time_difference >= 0.25){
            let time_container = document.createElement("div");
            event_container.append(time_container);
            time_container.classList.add("event-time");
            time_container.innerHTML += `${event_object["start_time"]}-${event_object["end_time"]}`;
            }else{
                if(time_difference <= 5/60 ){event_container.style.fontSize = "0.6rem"; }}
        }) 
        
    })
}
        
function clickbox(event , schedule_id, box_number, box_or_event, offset, event_details ){
    /* caters to both clicking an empty box or clicking an event
    box_or_event - differentiates whether box or event
    nb - event popups are not inherently appended to event container but to event boxes and then 
    shifted down with offset - in order to be able to have a higher global z-index than other event 
    containers */
    event.stopPropagation();
    
    //clear other popups on screen
    clear_popups();
    
    // use schedule id and box number to locate box which was clicked  
    let event_box = document.querySelector(`div[data-event="${box_number}"][data-schedule="${schedule_id}"]`);

    // popup form to submit ------------------------------------------------------
    let form = create_Form(schedule_id, event_details, box_number);
    event_box.append(form);

    form.firstChild.childNodes[1].firstChild.focus(); //let title input receive focus
    
    let top = 0; // initial offset of form

    if (box_or_event == "event"){
        top = offset; //if for event shift to meet event
    }
    
    //if box will go out of page shift form upwards 
    let height = form.offsetHeight; //height of form
    let shift_needed = event.y + height; //indicate we might need shifting

    if (shift_needed > window.innerHeight){
        shift_needed = form.getBoundingClientRect().top + top + height - window.innerHeight;

        if (shift_needed > 0 ){//if shift actually needed
            form.style.top = `${top - shift_needed}px`;

        }else{form.style.top = `${top}px`; }
        
    }else{
        form.style.top = `${top}px`;
    }
    
    form.classList.add("popup-form","animate");
    
    // if x coordinate is more than half the screen width popup to left of box instead of to right of box 
    let x = event.x;
    let half_screen_size = window.innerWidth * 3 / 5;

    if (x > half_screen_size){
        form.style.left = `-233%`;
        form.classList.add("slideInRight");
    }else{
        form.classList.add("slideInLeft");
    }

}

function create_Form(schedule_id, event_details, box_number){
    /* Creates forms different if event box or event */
    let form = document.createElement("form");
    let form_container = document.createElement("div");
    form.append(form_container);
    form_container.classList.add("container")

    let top = document.createElement("div");
    form_container.append(top);
    top.classList.add("top");


    if(event_details){
        //delete button
        let delete_event = document.createElement("span");
        delete_event.innerHTML += "delete";
        delete_event.classList.add("material-symbols-outlined", "pointer");
        top.append(delete_event);

        // deleting events ----------------------------------------------------------------------
        delete_event.addEventListener("click", async (event)=>{
            event.stopPropagation();
            let [object, status_code] = await myFetch(`api/Events/${event_details["id"]}`, "DELETE");
            if (eval_status_code(status_code)){
            load_schedule(event_details["schedule"])};

            flash_message(object["message"], status_code);
        })
    }

    let close = document.createElement("span");
    close.classList.add("pointer", "close");
    close.innerHTML += "&#215;";
    close.addEventListener("click", ()=>{
        clear_popups();
    })
    top.append(close);

    let middle = document.createElement("div");
    form_container.append(middle);

    let title_input = document.createElement("input");
    title_input.setAttribute("placeholder", "Add Title");
    title_input.setAttribute("name", "title");

    middle.append(title_input);

    let start_time = document.createElement("input");
    start_time.setAttribute("name", "start_time");
    start_time.setAttribute("placeholder", "Start");

    let end_time = document.createElement("input");
    end_time.setAttribute("name", "end_time");
    end_time.setAttribute("placeholder", "End");
    
    let time_div = document.createElement("div");
    time_div.classList.add("time");
    form_container.append(time_div);
    time_div.append(start_time, end_time);


    let bottom = document.createElement("div");
    form_container.append(bottom);

    let description = document.createElement("textarea");
    description.setAttribute("name", "description");
    description.setAttribute("placeholder", "Description");
    description.classList.add("description");
    bottom.append(description);

    let actual_bottom = document.createElement("div");
    form_container.append(actual_bottom);

    let overlap = document.createElement("input");
    overlap.setAttribute("name", "overlap");
    overlap.setAttribute("type", "checkbox");
    actual_bottom.append(overlap);

    // populate if event box
    if (event_details){
        title_input.value = event_details["title"];
        start_time.value = event_details["start_time"];
        end_time.value = event_details["end_time"];
        description.value = event_details["description"];
    }else{
        start_time.value = `${box_number}:00`;
    }
    
    let submit = document.createElement("button");
    submit.innerHTML += "Submit";
    actual_bottom.append(submit)


    form.addEventListener("click", (event)=>{
        //stop other click events happening when workin on the form especially to not allow listener that clears forms
        //receive event
        event.stopPropagation();
    })

    form.addEventListener("submit", async (event)=>{
        event.preventDefault();
        //if event details then  put else post
        let endpoint = event_details ? `api/Events/${event_details["id"]}/` : `api/Schedule/${schedule_id}/events`;
        let method =  event_details ? "PUT" : "POST";

        let [response, status_code] = await myFetch(endpoint, method, new FormData(form));
        
        if(eval_status_code(status_code)){
        load_schedule(response["object"]["schedule"])}
        flash_message(response["message"], status_code);
    })

    return form;
}


async function myFetch(endpoint, method="GET",body,  content_type=null){
    /* allows for me to get request result */
    if(content_type){
    let result = await fetch(endpoint, {
        method: method,
        headers:{
            Authorization: `Bearer ${localStorage.getItem("token")}`,
            "Content-Type": content_type

        },
        body: body})
        .then(async res => {return [await res.json(), res.status] })
        
    return result;}
    else{
        let result = await fetch(endpoint, {
            method: method,
            headers:{
                Authorization: `Bearer ${localStorage.getItem("token")}`,
    
            },
            body: body})
            .then(async res => {return [await res.json(), res.status] } )
            
        return result;
    }
}

function clear_screen(){
    /* clear screen mainly for calendar switching */

    //clear sidebar
    document.querySelector("#sidebar").innerHTML  = "";
    //clear grid
    document.querySelector(".label-col").innerHTML =  "";
    document.querySelectorAll(".schedule-col").forEach(column => column.innerHTML = "");

}

function clear_popups(){
    /* handles clearing of popup forms and menus and checkboxes*/
    let popups = document.querySelectorAll(".popup-form");
    popups.forEach((form)=>{
        form.classList.add("disappear");
        form.style.display = "none";
    }) 

    let menus = document.querySelectorAll(".sched-menu");
    menus.forEach((menu)=>{
        menu.classList.add("scaleOut");
        //menu.style.display = "none";
    }) 

    let checkboxes = document.querySelectorAll(".checkbox");
    checkboxes.forEach((checkbox)=>{
        checkbox.style.display = "none";})
    
    let new_forms = document.querySelectorAll(".new-form");
    new_forms.forEach((new_form)=>{
        new_form.style.display = "none";})

}

function parse_time(event){
    /* Function handling parsing of times */
    let start_time = event["start_time"];
    let end_time = event["end_time"];

    let start_hour = Number(start_time.substr(0,2));
    let end_hour = Number(end_time.substr(0,2));
    
    let start_minute = Number(start_time.substr(3,2));
    let end_minute = Number(end_time.substr(3,2));

    let time_difference = (end_hour + end_minute/60 )- (start_hour +  start_minute/60);
    let hour_difference = end_hour - start_hour;


    // if the end minute of an event is not 0; it crosses over into the next hour
    let crossover = (end_minute != 0) ? 1 : 0;

    //hacky 
    let gap_number = hour_difference - 1 + crossover;

    return [start_hour, start_minute, time_difference, hour_difference, gap_number, end_hour, end_minute];
}

function flash_message(message, status_code){
    /* Function handling display of messages */
    let container = document.createElement("div");
    container.innerHTML += `${message}`;

    let message_class = Number((status_code / 100).toFixed(0));
    let type;
    if ( message_class == 2){
        type = "success";
    }else{
        type = "failure";
    }

    container.classList.add("message", type, "disappear", "long");
    document.body.append(container);
}

function display_schedule_options(event, schedule){
    /* Dropdown menu for schedules and related functionality */
    clear_popups();
    event.stopPropagation();
    //box that was clicked
    let box = document.querySelector(`div[data-schedtitle="${schedule["id"]}"]`)

    //dropdown menu
    let menu = document.createElement("div");
    menu.classList.add("sched-menu", "animate", "slideInTop");

    if (event.x > window.innerWidth *3/4){
        menu.style.right = "0";
    }else{
        menu.style.left = "0";
    }
    box.append(menu);

    let copy = document.createElement("div");
    copy.innerHTML += "Copy";

    //copy schedules ---------------------------------------------------------------------
    copy.addEventListener("click", async (event)=> {
        event.stopPropagation();
        if (copy.children[0]){clear_children(copy)};//so as to not have many children
        //get all schedule titles
        let titles = document.querySelectorAll(".schedule-name");
        titles.forEach((title)=>{
            let other_id = title.getAttribute("data-schedtitle")
            if ( other_id != schedule["id"]){ //if title is not title that was clicked
            let checkbox = document.createElement("input");
            checkbox.addEventListener("click", event => event.stopPropagation())
            checkbox.setAttribute("type","checkbox")
            checkbox.setAttribute("data-schedid", other_id);
            checkbox.classList.add("checkbox");
            title.append(checkbox);}})//add checkbox
        
        let to_side = document.createElement("div");
        to_side.classList.add("to-side", "animate");

        //conditionally rendering to_side
        if (event.x > window.innerWidth *3/4){
            to_side.style.right = "105%";
            to_side.classList.add("scaleInRight");
        }else{
            to_side.style.left = "105%";
            to_side.classList.add("scaleInLeft");

        }
        copy.append(to_side)

        let done = document.createElement("div");
        let body = []; //hold id's to be copied to
        done.innerHTML += "Done";
        done.addEventListener("click", async (event)=>{
            event.stopPropagation();
            let titles = document.querySelectorAll(".checkbox");
            for(let i=0; i<titles.length; i++){
                if (titles[i].checked){
                body.push(titles[i].getAttribute("data-schedid"));
                }
            } 
           
            let [object, status_code] = await myFetch(`/api/Copy/Schedule/${schedule["id"]}/`, "PUT", 
            body= JSON.stringify({"schedules":body}),  content_type="application/json");
            console.log(object["message"]);
            clear_screen();
            load_home();
            flash_message(object["message"], status_code);           
        })
        to_side.append(done);

        let cancel = document.createElement("div");
        cancel.innerHTML += "Cancel";
        cancel.addEventListener("click", event=>{
            event.stopPropagation();
            clear_popups()});
        to_side.append(cancel);
    })
    

    let clear = document.createElement("div");
    clear.innerHTML += "Clear";
    clear.addEventListener("click", async (event)=> {
        event.stopPropagation();
        let [object, status_code] = await myFetch(`/api/Clear/Schedule/${schedule["id"]}/`,"PUT");
        console.log("schedule here", schedule);
        load_schedule(schedule)
        flash_message(object["message"], status_code)}
        )

    menu.append(copy,clear);
}


function eval_status_code(status_code){
    return Math.floor(status_code / 100) == 2;
}

function clear_children(node){
    node.children[0].remove();
}