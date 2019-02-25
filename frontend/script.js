window.onload=function(){
  var form = document.getElementById("uploadbanner");
  if (form){
    form.addEventListener("submit", callback, false);
  }

  function handleErrors(response) {
      if (!response.ok) {
          throw Error(response.statusText);
      }
      return response;
  }

  function callback (e) {
    //console.log("callback success!")
    e.preventDefault();
    //var url = "http://127.0.0.1:8080/api/schedule"
    var url = "http://localhost:8080/api/schedule"
    var formdata = new FormData(form);
    document.getElementById("statusinfo").innerHTML += "Files are submitted. Waiting for a schedule!<br>"
    fetch(url,{
      method: "POST",
      body: formdata
    }).
    then(handleErrors).
    then(result => {
      console.log(result)
      res = result.json()
      document.getElementById("statusinfo").innerHTML+= "Response received. Fetch succeeded. <br>"
      console.log(res)
      return res
    }).
    then(result => {
      console.log(result)
    }).
    catch(error => {
      console.log(error)
      document.getElementById("statusinfo").innerHTML+= error + "<br>"
    })

  }

}
