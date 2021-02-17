let slide_set = INSERT_SLIDES_HERE;

function populate() {
	let dd_html = "";
	for(let i=0; i!=slide_set.length; i++) {
		dd_html += `<option value="${i}">${slide_set[i]["title"]}</option>`;
	}

	document.getElementById("slide_selector").innerHTML = dd_html;
	document.getElementById("slide_selector").options[0].selected = true;
	swapSlide();
}

function swapSlide() {
	let dropdown = document.getElementById("slide_selector");
	const value = dropdown.options[dropdown.selectedIndex].value;
	const slide = slide_set[value];

	document.getElementById("slide_link").href = `https://voteview.com${slide["link"]}`;
	document.getElementById("slide_caption").innerHTML = slide["caption"];
	document.getElementById("slide_header").innerHTML = slide["title"];
	document.getElementById("prototype_title").value = slide["title"];
	document.getElementById("prototype_caption").value = slide["caption"];
	if(slide["video"] !== undefined) {
		document.getElementById("slide_image").style.display = "none";
		document.getElementById("slide_video").style.display = "inline";
		document.getElementById("slide_video").src = `../images/${slide["video"]}`;
	} else {
		document.getElementById("slide_image").style.display = "inline";
		document.getElementById("slide_image").src = `../images/${slide["image"]}`;
		document.getElementById("slide_video").src = "";
		document.getElementById("slide_video").style.display = "none";
	}

	if(slide["mask"] != undefined) {
		document.getElementById("slide_item").className = `item active item_${slide["mask"]}`;

		for(let i=0; i != document.getElementById("slide_mask").options.length; i++) {
			if(slide["mask"] == document.getElementById("slide_mask").options[i].value) { 
				document.getElementById("slide_mask").options[i].selected = true;
				break;
			}
		}
	} else {
		document.getElementById("slide_item").className = "item active";
	}


}

function swapMask() {
	let dropdown = document.getElementById("slide_mask");
	const value = dropdown.options[dropdown.selectedIndex].value;

	if(value) {
		document.getElementById("slide_item").className = `item active item_${value}`;
	} else {
		document.getElementById("slide_item").className = "item active";
	}
}

function updateSlide() {
	document.getElementById("slide_header").innerHTML = document.getElementById("prototype_title").value;
	document.getElementById("slide_caption").innerHTML = document.getElementById("prototype_caption").value;
}

populate();
