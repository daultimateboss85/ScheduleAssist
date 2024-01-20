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


/**
 * This function is true if status_code is 2xx
 * @param {number} status_code
 * @returns {boolean}
 *  */  

function eval_status_code(status_code){
    return Math.floor(status_code / 100) == 2;
}


export {myFetch, eval_status_code}