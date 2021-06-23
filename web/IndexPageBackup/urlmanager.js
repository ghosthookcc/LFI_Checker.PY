getfile = (url) => {
	let xhrResponse = new XMLHttpRequest();
	let completeStr = ""

	xhrResponse.onreadystatechange = function() 
	{
 		if (xhrResponse.readyState === 4 && xhrResponse.status === 200) 
 	 	{
 	 		text = xhrResponse.responseText;
 	 		lines = text;
 	 		for(i = 0; i < lines.length; i++) {
 	 			completeStr += lines[i];
 	 		}
  	 	}
   	}
   	xhrResponse.open('GET', url, true);
	xhrResponse.send('');
}

const url = "urls.txt";
getfile(url);

/*
let obj = { first: "John", last: "Doe" };

Object.keys(obj).forEach(function(key) {
	console.log(key, obj[key]);
});
*/

let downloadImg = document.querySelectorAll(".downloadImg");

for(i = 0; i < downloadImg.length; i++) {
	downloadImg[i].addEventListener("mouseover", func = (event) => {

		// console.log("Is it working?");
		event.target.src = "img/downloadfilemouseover.png";
	});
	
	downloadImg[i].addEventListener("mouseleave", func = (event) => {
		event.target.src = "img/downloadfile.png";
	});
}
