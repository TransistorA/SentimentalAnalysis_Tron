window.onload=function(){
  var form = document.getElementById("uploadbanner");
  if (form){
    form.addEventListener("submit", callback, false);
  }

  function callback (e) {
    //console.log("callback success!")
    e.preventDefault();
    var url = "http://127.0.0.1:8080/api/schedule"
    var formdata = new FormData(form);
    document.getElementById("statusinfo").innerHTML="Files are submitted. Waiting for a schedule!"
    fetch(url,{
      method: "POST",
      body: formdata
    }).
    then(result => {
      console.log(result)
      res = result.json()
      console.log(res)
      return res
    }).
    then(result => {
      console.log(result)
    })

  }

}
