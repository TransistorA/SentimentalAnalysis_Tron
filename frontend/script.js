window.onload=function(){
  var form = document.getElementById("uploadbanner");
  console.log("script success!")
  if (form){
    form.addEventListener("submit", callback);
    console.log("form success!")
  }
}
function callback () {
  console.log("callback success!")
  url = "http://localhost:8080/api/schedule"
  fetch(url,{method: "POST"}).
  then(result => {
    console.log("submit success!")
  }
  )
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
