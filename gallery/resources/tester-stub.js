let slide_set = INSERT_SLIDES_HERE;

function populate() {
	let dd_html = "";
	for(let i=0; i!=slide_set.length; i++) {
		dd_html += `<option value="${i}">${slide_set[i]["header"]}</option>`;
	}

	document.getElementById("slide_selector").innerHTML = dd_html;
	document.getElementById("slide_selector").options[0].selected = true;
	swapSlide();
}

function swapSlide() {
	let dropdown = document.getElementById("slide_selector");
	const value = dropdown.options[dropdown.selectedIndex].value;
	const slide = slide_set[value];

	document.getElementById("slide_link").href = slide["link"];
	document.getElementById("slide_caption").innerHTML = slide["caption"];
	document.getElementById("slide_header").innerHTML = slide["title"];
	if(slide["video"] !== undefined) {
		document.getElementById("slide_image").style.display = "none";
		document.getElementById("slide_video").style.display = "inline";
		document.getElementById("slide_video").src = slide["video"];
	} else {
		document.getElementById("slide_image").style.display = "inline";
		document.getElementById("slide_image").src = slide["image"];
		document.getElementById("slide_video").src = "";
		document.getElementById("slide_video").style.display = "none";
	}

	if(slide["mask"] != undefined) {
		document.getElementById("slide_item").className = `item item_${slide["mask"]}`;
	} else {
		document.getElementById("slide_item").className = "item";
	}

	document.getElementById("slide_mask").options[0].selected = true;
}

function swapMask() {
	let dropdown = document.getElementById("slide_mask");
	const value = dropdown.options[dropdown.selectedIndex].value;

	if(value) {
		document.getElementById("slide_item").className = `item item_${value}`;
	} else {
		document.getElementById("slide_item").className = "item";
	}
}

populate();
