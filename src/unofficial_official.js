// data is loaded before this.

var select = document.createElement('select');
select.addEventListener("change", changeEvents);


var event_select = document.createElement('select');

for (var op in data) {
	var option = document.createElement('option');
	option.innerHTML = op;
	select.appendChild(option);
}


function changeEvents(){
	event_select.innerHTML = "";
	var region = select.options[select.selectedIndex].value;
	for (var event in data[region]) {
		var option = document.createElement('option');
		option.innerHTML = event;
		event_select.appendChild(option);
	}
	console.log(region);
}

document.body.appendChild(select);
document.body.appendChild(event_select);

changeEvents();