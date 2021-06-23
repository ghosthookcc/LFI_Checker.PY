let downloadImg = document.querySelectorAll(".downloadImg");

for(i = 0; i < downloadImg.length; i++) {
	downloadImg[i].addEventListener("mouseover", func = (event) => {
		event.target.src = "img/downloadfilemouseover.png";
	});

	downloadImg[i].addEventListener("mouseleave", func = (event) => {
		event.target.src = "img/downloadfile.png";
	});
}

let textareas = document.getElementsByTagName("TEXTAREA");

for(i = 0; i < textareas.length; i++)
{
	textareas[i].setAttribute("readonly", "True");
}
