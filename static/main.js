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


    fetch("api/ScheduleCalendars/", {
        headers:{
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
    })
    .then(res => res.json())
    .then(result => {
        console.log(result)
    })
})