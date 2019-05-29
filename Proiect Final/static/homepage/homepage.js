SERVER = " http://127.0.0.1:9005";

let current_pin_id;
let current_pin_lat;
let current_pin_lng;
let current_image = "";
let first_time = true;
let image_content = "";

//------------------
// -- Google Map ---
//------------------
let map;

// Take the user's coordinates.
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(successFunction);
} else {
    alert('It seems like Geolocation is not enabled in your browser.');
}

Swal.fire({
  text: 'Your videos are on their way... Hold On !',
  width: 650,
  padding: '3em',
  showConfirmButton: false,
  allowOutsideClick: false,
    allowEscapeKey: false,
  backdrop: `
    #ffffff
    url("static/homepage/nyan-cat.gif")
    center left
    no-repeat
`});


// On getting coordinates, initialize map.
// Also initialize search
function successFunction(position) {
    let lati = position.coords.latitude;
    let long = position.coords.longitude;
    // We initialize Map with user coordinates
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: lati, lng: long},
        fullscreenControl: false,
        zoom: 13
    });

    // Adding click listener to add pinpoints
    map.addListener('click', function(e1) {
        // ASK user for movie
        const input = document.createElement('input');
        input.type = 'file';
        input.onchange = e => {
            // 1. Place the marker
            placeMarker(e1.latLng, map);
            // 2. Send marker location to server
            let data1 = JSON.stringify(e1.latLng);
            let xhr1 = new XMLHttpRequest();
            const data = new FormData();
            console.log(e.target.files[0]);
            data.append("file", e.target.files[0]);

            xhr1.addEventListener("readystatechange", function () {
              if (this.readyState === 4) {
                    let pinId = this.responseText;
                    //3. Send movie to server
                    const xhr = new XMLHttpRequest();
                    xhr.addEventListener("readystatechange", function () {
                        console.log(this.responseText);
                    });
                    xhr.open("POST", SERVER+"/upload/movies/"+pinId);
                    xhr.setRequestHeader("cache-control", "no-cache");
                    console.log(data);
                    xhr.send(data);
              }});
            xhr1.open("POST", SERVER+"/upload/pins");
            xhr1.setRequestHeader("Content-Type", "application/json");
            xhr1.setRequestHeader("cache-control", "no-cache");
            xhr1.send(data1);
        };
        input.click();
    });

    // Search
    let search = document.getElementById("search");
    let autocomplete = new google.maps.places.Autocomplete(search);
    autocomplete.addListener('place_changed', function() {
          let place = autocomplete.getPlace();
          map.setCenter(place.geometry.location);
    });
}

// Add pins on the map
function setPins(){

    let xhr = new XMLHttpRequest();
    xhr.addEventListener("readystatechange", function () {
    if (this.readyState === 4) {
        console.log(this.responseText);
        let pinsArray = JSON.parse(this.responseText);
        for (let i = 0; i < pinsArray.length; i++) {
            placeMarker(pinsArray[i]);
        }
        Swal.close();
    }});
    xhr.open("GET", SERVER+"/pins");
    xhr.setRequestHeader("cache-control", "no-cache");
    xhr.send();
}
setPins();

//-----------------
// -- Pinpoints ---
//-----------------
// Add actions to pinpoints click
function placeMarker(location) {
    // We add marker to map
    let marker = new google.maps.Marker({
        position: location,
        animation: google.maps.Animation.DROP,
        map: map
    });
    marker.set("id", location.id);
    marker.addListener('click', function() {
        first_time = false;
        // We set current pin ID, LAT, LNG
        current_pin_id = marker.id;
        current_pin_lat = location.lat;
        current_pin_lng = location.lng;
        // 1. Open Windows and Set Title
        openWindow(current_pin_id);
        // 1. Open Sidebar
        // sidebarWindowOpen();
        // // 2. Set Title
        // setTitle();
        // 3. Set Messages in list
        // getMessages();
    });
}

function openWindow(current_pin_id) {
    console.log(current_pin_id);
    const div_map = document.getElementById("map");

    let geocoder = new google.maps.Geocoder;
    let latlng = {lat: current_pin_lat, lng: current_pin_lng};
    geocoder.geocode({'location': latlng}, function (results, status) {
        if (status === 'OK') {
            if (results[0]) {
                var xhr = new XMLHttpRequest();
                xhr.addEventListener("readystatechange", function () {
                if (this.readyState === 4) {
                    if (JSON.parse(this.responseText)[0].publicurl !== 'undefined' ) {
                        let  resp = JSON.parse(this.responseText)[0];
                    console.log( );
                    jsPanel.create({
                    theme: "light",
                    headerTitle: results[0].formatted_address,
                    position: 'center-top 0 58',
                    container: div_map,
                    contentSize: '400 500',
                    borderRadius: 0,
                    boxShadow: 1,
                    syncMargins: true,
                    contentOverflow: 'hidden',
                    headerControls: { smallify: "remove", maximize: "remove" },
                    dragit: { opacity: 1 },
                    content: "<video controls autoplay width='400' height='230' style='background-color: black;'><source src="+JSON.parse(this.responseText)[0].publicurl+" type='video/mp4'></video>"+
                        "<!--List area-->\n" +
                        "<span class='title-v'>Awsome Title</span>"+
                        "<div id=\"messages\">\n" +
                        "<ul class=\"list\"></ul>\n" +
                        "</div>"+
                        "<div class=\"message-warper\">\n" +
                        "<input type=\"text\" class=\"message\" placeholder=\"Write a message... \">\n" +
                        "<i class=\"material-icons attach\">add_circle</i>\n" +
                        "</div>",
                    callback: function (panel) {
                        const title_v = document.getElementsByClassName("title-v")[0];
                        let t1 = resp.filename.split('.').slice(0, -1).join('.');
                        let t2 = t1.replace(/_/g,' ');
                        title_v.innerHTML =  capLetter(t2);
                        console.log(resp);
                        // title_v.innerHTML = JSON.parse(this.responseText)[0].filename;
                        let message = document.getElementsByClassName("message")[0];
                        let messagesList = new List('messages', options);
                        message.addEventListener("keydown", function(event) {
                            console.log("Here");
                            if (event.key === "Enter") {
                                event.preventDefault();
                                // If message is not empty
                                if (message.value !== ""){
                                    let time = moment().format('LTS');
                                    // 1. Send message to server
                                    sendMessageToServer(message.value,time);
                                    // 2. Refresh list
                                    addMessage(message.value,time);
                                    // 3. Clear add box
                                    message.value="";
                                }
                            }
                        });
                        function addMessage(message,timestamp) {
                        if (image_content === "") {
                           messagesList.add({
                            message_body: message,
                            timestamp: timestamp
                        });
                        } else {
                            messagesList.add({
                            message_body: message,
                            timestamp: timestamp,
                            image: image_content
                        });}
                        }
                        function sendMessageToServer(message,time){
                        let data = new FormData();
                        data.append("pinid", current_pin_id);
                        data.append("file", current_image);
                        data.append("message",message);
                        data.append("time",time);

                        let xhr = new XMLHttpRequest();
                        xhr.open("POST", SERVER+"/upload/messages");
                        xhr.setRequestHeader("cache-control", "no-cache");
                        xhr.send(data);
                        current_image = ""
                        }
                        function capLetter(string) { return string.charAt(0).toUpperCase() + string.slice(1); }
                        // 3. Set Messages in list
                        function getMessages() {
                        let xhr = new XMLHttpRequest();
                        xhr.addEventListener("readystatechange", function () {
                          if (this.readyState === 4) {
                            setMessagesInList(this.responseText);
                          }
                        });
                        xhr.open("GET", SERVER+"/messages/"+current_pin_id);
                        xhr.setRequestHeader("cache-control", "no-cache");
                        xhr.send();
                        }
                        getMessages();
                        function setMessagesInList(response){
                        messagesList.clear();
                        if (response !== "") {
                            let messagesArray = JSON.parse(response);
                            for (let i = 0; i < messagesArray.length; i++) {
                                console.log(messagesArray[i].publicurl);
                                if (messagesArray[i].publicurl !== "") {
                                    messagesList.add({
                                        message_body: messagesArray[i].message,
                                        timestamp: messagesArray[i].time,
                                        image: messagesArray[i].publicurl
                                    });
                                }else {
                                    messagesList.add({
                                        message_body: messagesArray[i].message,
                                        timestamp: messagesArray[i].time,
                                        image: "http://1x1px.me/FFFFFF-1.png"
                                    });
            }
        }
    }
}
                        // Attach
                        const template = document.getElementById('add_tooltip');
                        const container = document.createElement('div');
                        template.style.display = 'block';
                        container.appendChild(document.importNode(template.content, true));
                        tippy('.attach', {
                            content: container.innerHTML,
                            arrow: true,
                            arrowType: 'round',
                            theme: 'light-border',
                            interactive: true,
                            trigger: 'click',
                            placement: 'top',
                            onShown(instance) {
                                let add_image = document.getElementsByClassName("add_image")[0];
                                add_image.addEventListener("click", set_image_file)
                            }
                        });
                        function set_image_file() {
                            let attach = document.getElementsByClassName("attach")[0];
                            let input = document.createElement('input');
                            input.type = 'file';
                            input.onchange = e => {
                                let file = e.target.files[0];
                                if (file !== "") {

                                    // setting up the reader
                                    let reader = new FileReader();
                                    reader.readAsDataURL(file); // this is reading as data url

                                    reader.onload = readerEvent => {
                                         // this is the content!
                                        image_content = readerEvent.target.result;
                                    };

                                    current_image = file;
                                    attach.style.color = "#005eb8"
                                }
                            };
                            input.click();
                        }
                    }
                });}
                }});
                xhr.open("GET", SERVER+"/movies/"+current_pin_id);
                xhr.send();
            }
        }
    });
}



// -- Sidenav --
// -- Initialization --
document.addEventListener('DOMContentLoaded', function() {
    let elems = document.querySelectorAll('.sidenav');
    console.log(elems);
    M.Sidenav.init(elems);
});

// -- List --
let options = {
  valueNames: [ 'message_body','timestamp', { attr: 'src', name: 'image'}],
  // Since there are no elements in the list, this will be used as template.
  item: '<li><p class="message_body"></p><span class="timestamp"></span><img class="image"></li>'
};


