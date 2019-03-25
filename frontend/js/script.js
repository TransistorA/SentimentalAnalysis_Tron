//Reference
//https://stackoverflow.com/questions/21012580/is-it-possible-to-write-data-to-file-using-only-javascript

var csvStr = ""
var textFile = null

makeTextFile = function(text) {
    var data = new Blob([text], { type: 'text/plain' });

    // If we are replacing a previously generated file we need to
    // manually revoke the object URL to avoid memory leaks.
    if (textFile !== null) {
        window.URL.revokeObjectURL(textFile);
    }

    textFile = window.URL.createObjectURL(data);

    // returns a URL you can use as a href
    return textFile;
};

window.onload = function() {
    var form = document.getElementById("uploadbanner");
    if (form) {
        form.addEventListener("submit", callback, false);
    }

    var save = document.getElementById("saveform");
    if (save) {
        save.addEventListener("submit", saveFunction, false);
    }

    function handleErrors(response) {
        if (!response.ok) {
            throw Error(response.statusText);
        }
        return response;
    }

    function saveFunction(e) {
        e.preventDefault();
        var link = document.createElement('a');
        filename = document.getElementById("filename").value + ".csv"
        link.setAttribute('download', filename);
        link.href = makeTextFile(csvStr);
        document.body.appendChild(link);

        // wait for the link to be added to the document
        window.requestAnimationFrame(function() {
            var event = new MouseEvent('click');
            link.dispatchEvent(event);
            document.body.removeChild(link);
        });
    }

    function callback(e) {
        //console.log("callback success!")
        e.preventDefault();
        //var url = "http://127.0.0.1:8080/api/schedule"
        var url = "http://localhost:8080/api/schedule"
        var formdata = new FormData(form);
        document.getElementById("statusinfo").innerHTML += "Files are submitted. Waiting for a schedule!<br>"
        fetch(url, {
            method: "POST",
            body: formdata
        }).
        then(handleErrors).
        then(result => {
            console.log(result)
            res = result.json()
            document.getElementById("statusinfo").innerHTML += "Response received. Fetch succeeded. <br>"
            console.log(res)
            return res
        }).
        then(result => {
            console.log(result)
            if (result["error"] == false) {
                document.getElementById("errormsg").innerHTML = ""
                document.getElementById("schedule").innerHTML = result["schedule"]
                csvStr = result["schedule"]
                document.getElementById("save").disabled = false
            } else {
                document.getElementById("errormsg").innerHTML = result["error_message"]
            }
        }).
        catch(error => {
            console.log(error)
            document.getElementById("statusinfo").innerHTML += error + "<br>"
            csvStr = ""
            document.getElementById("save").disabled = true
        })

    }

}