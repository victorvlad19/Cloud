// Incarca Continutul Pagini
const http_get = new XMLHttpRequest();
http_get.open("GET", "http://127.0.0.1:8000/interface");
http_get.send();
http_get.onload = () => {
    document.body.innerHTML = http_get.responseText;
    const start_button = document.getElementsByClassName("request");
    // Butonul de start
    start_button[0].addEventListener('click', function () {
        const hello = document.getElementsByClassName("picker")[0].value;
        console.log(hello);
        post_content(hello);
        window.alert("Starting...Hold on");
    });
    // Buttonul de log
    const logs = document.getElementsByClassName("log");
    logs[0].addEventListener('click', function () {
        window.location.href = "http://127.0.0.1:8000/metrics";
    });


};

function post_content(hello) {
    const http_post = new XMLHttpRequest();
    const json = JSON.stringify(hello);
    http_post.open("POST", "http://127.0.0.1:8000");
    //Send header information
    http_post.setRequestHeader("Content-Type", "application/json");
    http_post.send(json);
    http_post.onload = () => {
        const content = document.getElementsByClassName("content");
        let json_data = JSON.parse(http_post.responseText);

        for (let data in json_data) {
            console.log(json_data[data]);
            const node = document.createElement("LI");
            const textnode = document.createTextNode(json_data[data]);
            node.appendChild(textnode);
            content[0].appendChild(node);
        }
    }
}


