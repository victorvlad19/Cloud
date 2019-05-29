const server = window.location.href;

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

// Get all the video and added them to the grid
let xhr = new XMLHttpRequest();
xhr.addEventListener("readystatechange", function () {
  if (this.readyState === 4) {
      Swal.close();
      const add_toolbar = document.getElementsByClassName("add-toolbar")[0];
      add_toolbar.style.visibility = "visible";
      const title_1 =document.getElementsByClassName("title-1")[0];
      title_1.style.visibility = "visible";

      let array = JSON.parse(this.responseText);
      for (let i=0; i<array.length; ++i){
          console.log(array[i]);
          buildUserUI(array[i]);
      }
  } else { console.log("Loading...") }
});
xhr.open("GET", server+"video-list");
xhr.send();

// Build user interface for video
function buildUserUI(dict) {
    const grid_container = document.getElementsByClassName("grid-container")[0];
    let grid_card = document.createElement('div');
    grid_card.setAttribute("class","video-card card-shadow grid-item");
    grid_card.setAttribute("id", dict.url);
    let cardImage = document.createElement("div");
    cardImage.setAttribute("class","cardImage border-tlr-radius");
    let video = document.createElement('video');
    video.setAttribute("width","100%");
    video.src = dict.url;
    video.height = 166;
    video.addEventListener('loadedmetadata', function() {
        console.log(this.duration);
        let p = document.createElement("p");
        p.setAttribute("class","video-title");
        let t1 = dict.filename.split('.').slice(0, -1).join('.');
        let t2 = t1.replace(/_/g,' ');
        p.appendChild(document.createTextNode(lMare(t2)));

        grid_card.addEventListener("click",function () {
            console.log("Hello");

            let xhr = new XMLHttpRequest();

            xhr.addEventListener("readystatechange", function () {
            if (this.readyState === 4) {

                let response = JSON.parse(this.responseText);
                console.log(response);

                jsPanel.create({
                    theme: "light",
                    headerTitle: p.innerHTML ,
                    position: 'center-top 0 108',
                    borderRadius: 0,
                    headerControls: 'xs',
                    boxShadow: 1,
                    syncMargins: true,
                    contentSize: {width: 650, height: 360},
                    dragit: { opacity: 1 },
                    content: "<video controls autoplay width='640' height='360'><source src="+grid_card.id+" type='video/mp4'></video>" +
                        "<div class='similar'></div>",
                    callback: function (panel) {
                        const similar = document.getElementsByClassName("similar")[0];
                        let p = document.createElement("span");
                        p.setAttribute("class","also-like");
                        p.appendChild(document.createTextNode("You may also like ..."));
                        similar.appendChild(p);

                        for (let i=0; i< response.value.length; ++i){
                            similar.appendChild(createElementFromHTML(response.value[i].embedHtml));
                            console.log(response.value[i].embedHtml);
                        }
                        console.log(similar);
                    }

                });

            }});

            xhr.open("GET", server+"similar/"+p.innerHTML);
            xhr.send();

        });


        let span = document.createElement("span");
        span.setAttribute("class", "video-start");
        span.appendChild(document.createTextNode("Click to Open"));
        cardImage.appendChild(video);
        cardImage.appendChild(p);
        cardImage.appendChild(span);
        grid_card.appendChild(cardImage);
        grid_container.appendChild(grid_card);
    });
}

function lMare(string) { return string.charAt(0).toUpperCase() + string.slice(1); }
function createElementFromHTML(htmlString) {
    console.log(htmlString);
    let myStr1 = htmlString.replace(/1280/g, '640');
    let myStr2 = myStr1.replace(/720/g, '360');
    let myStr3 = myStr2.replace(/autoplay=1/g, 'autoplay=0');
    let div = document.createElement('div');
    div.innerHTML = myStr3.trim();
    return div.firstChild;
}

// Add movie click listener
const add_toolbar = document.getElementsByClassName("add-toolbar")[0];
add_toolbar.addEventListener("click",function () {
    const input = document.createElement('input');
    input.type = 'file';
    input.onchange = e => {
        const data = new FormData();
        console.log(e.target.files[0]);
          data.append("file", e.target.files[0]);
          const xhr = new XMLHttpRequest();
            xhr.addEventListener("readystatechange", function () {
                console.log(this.responseText);
            });
            xhr.open("POST", server+"upload");
            xhr.setRequestHeader("cache-control", "no-cache");
            console.log(data);
            xhr.send(data);
    };
    input.click();
});