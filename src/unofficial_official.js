// data is loaded before this.

var select = document.createElement('select');
select.addEventListener("change", changeEvents);

var event_select = document.createElement('select');
event_select.addEventListener("change", showChampions);

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
	showChampions();
}

function showChampions(){
	var region = select.options[select.selectedIndex].value;
	var event = event_select.options[event_select.selectedIndex].value;

	table_div.innerHTML = "";
	var table = document.createElement('table');
	for (var i=0; i<data[region][event]["champions"].length; i++){
		var tr = document.createElement('tr');

		var name_td = document.createElement('td');
		name_td.innerHTML = data[region][event]["champions"][i]["champion_name"];
		tr.appendChild(name_td);

		var competition_td = document.createElement('td');
		competition_td.innerHTML = data[region][event]["champions"][i]["competition"];
		tr.appendChild(competition_td);

		table.appendChild(tr);
	}
	table_div.appendChild(table);
}

document.body.appendChild(select);
document.body.appendChild(event_select);

var table_div = document.createElement('div')
document.body.appendChild(table_div);

changeEvents();