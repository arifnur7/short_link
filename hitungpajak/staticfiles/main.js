/*let form = document.getElementById("form")
form.addEventListener("submit", function (ev){
    ev.preventDefault()
    async function makeRequest(url, method, body){
        let headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json'
        }

        if (method == "post"){
            const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value
            headers['X-CSRFToken'] = csrf
        }

        let response = await fetch('{% url "post" %}', {
            method: method,
            headers: headers,
            body:body
        })
        return await response.json()
    }
    async function getNumber (){

        const data = await makeRequest('{% url "post" %}', 'get')

        let from = document.getElementById('form')

    }

    async function getFloatNumber(e){
        let number = e.target.innerText

        let data = await makeRequest('{% url "post" %}', method = 'post', body = JSON.stringify({number:number}))
    }
})*/

// //---- cara frisca ----
// document.addEventListener("DOMContentLoaded", function() {
//     document.querySelector("form").addEventListener("submit", function(e) {
//         e.preventDefault();
//         var formData = new FormData(this);
//         var xhr = new XMLHttpRequest();
//         xhr.open("POST", '{% url "result" %}', true);
//         xhr.onload = function() {
//             if (xhr.status === 200) {
//                 var element = document.getElementById('form');
//                 var copy = document.getElementById('load'); // Clone the element
//                 element.appendChild(copy);
//
//             }
//         };
//         xhr.send(formData);
//     });
// });

// cara dari ChatGPT
document.querySelector("form").addEventListener("submit", function(event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Get the URL from the data attribute
    let postUrl = document.querySelector("form").action;
    let container = document.querySelector("#result")
    // Gather form data
    let formData = new FormData(document.querySelector("form"));
    fetch(postUrl,{method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': '{{ csrf_token }}'  // Include CSRF token
        },})
        .then(response => response.text())  // Assuming the server returns plain text or HTML
        .then(text => {
        // Update the body content with the received text
            container.innerHTML = text;
        }).catch(error => {
            console.error('Error:', error);
        })
})


//     // Send POST request with form data using AJAX
//     var xhr = new XMLHttpRequest();
//     xhr.open("POST", postUrl, true);
//     xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
//     xhr.onreadystatechange = function() {
//         if (xhr.readyState === XMLHttpRequest.DONE) {
//             if (xhr.status === 200) {
//                 // Handle successful response
//                 var response = JSON.parse(xhr.responseText);
//                 console.log(response);
//
//                 // Update DOM elements with the received data
//                 document.getElementById("nama_barang").textContent = 'Nama barang: '+ response.nama_barang;
//                 document.getElementById("jenis_barang").textContent = 'Jenis Barang: '+response.jenis_barang;
//                 document.getElementById("bea_masuk").textContent = 'Bea Masuk: '+response.bea_masuk+' %';
//                 document.getElementById("formatted_cost").textContent = 'Harga Barang: Rp.'+response.formatted_cost;
//                 document.getElementById("formatted_insurance").textContent = 'Nilai Asuransi: Rp.'+response.formatted_insurance;
//                 document.getElementById("formatted_freight").textContent = 'Biaya Kirim: Rp.'+response.formatted_freight;
//                 document.getElementById("formatted_cif").textContent = 'CIF (Cost-Insurance-Freight) :Rp.'+response.formatted_cif;
//                 document.getElementById("formatted_dpp").textContent = 'Dasar Pengenaan Pajak (DPP) : Rp.'+response.formatted_dpp;
//                 document.getElementById("formatted_result").textContent = 'Hasil Hitung DPP dikalikan PPN Rp.'+response.formatted_result;
//
//
//             } else {
//                 // Handle error response
//                 console.error('Request failed:', xhr.status);
//             }
//         }
//     };
//     xhr.send(formData);
// });
