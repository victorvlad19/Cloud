SERVER = "https://cloudweek7.appspot.com";

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
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(successFunction);
} else {
    alert('It seems like Geolocation is not enabled in your browser.');
}

function successFunction(position) {
    let lati = position.coords.latitude;
    let long = position.coords.longitude;
   
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: lati, lng: long},
        fullscreenControl: false,
        zoom: 13
    });
    
    map.addListener('click', function(e) {
        placeMarker(e.latLng, map);
        sendLocationOf_PINPOINTS_ToServer(e.latLng);
    });

    let search = document.getElementById("search");
    let autocomplete = new google.maps.places.Autocomplete(search);

    autocomplete.addListener('place_changed', function() {
          let place = autocomplete.getPlace();
          map.setCenter(place.geometry.location);
    });
}

function sendLocationOf_PINPOINTS_ToServer(location){
    let data = JSON.stringify(location);
    let xhr = new XMLHttpRequest();
    xhr.addEventListener("readystatechange", function () {
      if (this.readyState === 4) {
        console.log(this.responseText);
      }
    });
    xhr.open("POST", SERVER+"/upload/pins");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("cache-control", "no-cache");
    xhr.send(data);
}

function setPins(){
    let xhr = new XMLHttpRequest();
    xhr.addEventListener("readystatechange", function () {
    if (this.readyState === 4) {
        let pinsArray = JSON.parse(this.responseText);
        for (let i = 0; i < pinsArray.length; i++) {
            placeMarker(pinsArray[i]);
        }
    }});
    xhr.open("GET", SERVER+"/pins");
    xhr.setRequestHeader("cache-control", "no-cache");
    xhr.send();
}
setPins();

//-----------------
// -- Pinpoints ---
//-----------------
function placeMarker(location) {
    let marker = new google.maps.Marker({
        position: location,
        animation: google.maps.Animation.DROP,
        map: map
    });
    marker.set("id", location.id);
    marker.addListener('click', function() {
        first_time = false;
       
        current_pin_id = marker.id;
        current_pin_lat = location.lat;
        current_pin_lng = location.lng;
     
        sidebarWindowOpen();
        setTitle();
        getMessages();
    });
}

function sidebarWindowOpen(){
    let elems = document.querySelectorAll('.sidenav');
    let instance = M.Sidenav.getInstance(elems[0]);
    instance.open();
}

function setTitle() {
    let title = document.getElementsByClassName("zone-title")[0];
    let geocoder = new google.maps.Geocoder;
    let latlng = {lat: current_pin_lat, lng: current_pin_lng};
    geocoder.geocode({'location': latlng}, function (results, status) {
        if (status === 'OK') {
            if (results[0]) {
                title.innerHTML = results[0].formatted_address;
            }
        }
    });
}

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

// -- Sidenav --
// -- Initialization --
document.addEventListener('DOMContentLoaded', function() {
    let elems = document.querySelectorAll('.sidenav');
    console.log(elems);
    M.Sidenav.init(elems);
});

let sidebar_open = document.getElementsByClassName("sidebar-open")[0];
sidebar_open.addEventListener("click",function () {
    let elems = document.querySelectorAll('.sidenav');
    let instance = M.Sidenav.getInstance(elems[0]);
    if (first_time === false) {
        instance.open();
    } else {
         M.toast({html: 'First time you must click on a pin !'})
    }
});

// -- More Button --
tippy('.more_options', {
    content: "Delete",
    arrow: true,
    arrowType: 'round',
    theme: 'light-border',
    interactive: true,
    placement: 'right',
});

// -- List --
let options = {
  valueNames: [ 'message_body','timestamp', { attr: 'src', name: 'image'}],
  item: '<li><p class="message_body"></p><span class="timestamp"></span><img class="image"></li>'
};
let messagesList = new List('messages', options);

let message = document.getElementsByClassName("message")[0];
message.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        if (message.value !== ""){
            let time = moment().format('LTS');
            sendMessageToServer(message.value,time);
            addMessage(message.value,time);
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
            let reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = readerEvent => {
                image_content = readerEvent.target.result;
            };

            current_image = file;
            attach.style.color = "#005eb8"
        }
    };
    input.click();
}