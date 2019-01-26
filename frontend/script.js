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




/*
  var breeddict = "https://dog.ceo/api/breeds/list/all"
  var randombreed = "https://dog.ceo/api/breed/hound/images/random"
  console.log("1")
  fetch(breeddict)
    .then(resp=>{
      return resp.json()
    })
    .then(json=>{
	  var breedlist = []
	  for (var key in json.message){
		  breedlist.push(key)
	  }
	  var breed = breedlist[Math.floor(Math.random()*breedlist.length)]
	  document.getElementById("breed")
		.innerHTML = '<div id="breed">Breed: '+ breed +'</div>'
	  console.log(breed)
	  fetch(randombreed)
		.then(resp=>{
			return resp.json()
		})
		.then(json=>{
			var imgsourse = json.message
			console.log(imgsourse)
			document.getElementById("img_container")
				.innerHTML = '<img src="'+ imgsourse +'">'
		})
		.catch(error => console.log("ERROR"+error))

    })
	.catch(error => console.log("ERROR"+error))
}


document.getElementById("random")
.addEventListener('click', loadAjax)
*/
