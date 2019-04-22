import {updateSelectParameter, getParameterByName, setSelectValue, updateQueryParameter} from './useQueryParameter.js';

// data is loaded before this.

var container = document.createElement('div');
container.setAttribute("class", "container text-center");

var title = document.createElement('h2');
title.classList.add("text-center");
title.innerHTML = "Unofficial official champion";
container.appendChild(title);

var explanation = document.createElement('p');
explanation.innerHTML = "The first unofficial official champion in an event is the best placed competitor of that event in the first regional championship.\n" +
                        "The competitor of the same region who beats the unofficial official champion bebomes the new unofficial official champion.\n" +
                        "If a champion does not compete for 1 year, the title fall for the better placed competitor in the last competition of the inactive former champion.\n"+
                        "Title is shared in case of tie. This stat is yet experimental, please report any issue if you find.";
container.appendChild(explanation);

var select = document.createElement('select');
select.addEventListener("change", changeEvents);
container.appendChild(select);

var event_select = document.createElement('select');
event_select.addEventListener("change", showChampions);
container.appendChild(event_select);

Object.keys(data).sort().forEach(region => {
    var option = document.createElement('option');
    option.innerHTML = region;
    select.appendChild(option);
});

function changeEvents(){
    event_select.innerHTML = "";
    var region = select.options[select.selectedIndex].value;
    for (var event in data[region]) {
        var option = document.createElement('option');
        option.innerHTML = event;
        event_select.appendChild(option);
    }
    updateQueryParameter("region", region);
    showChampions();
}

function showChampions(){
    var region = select.options[select.selectedIndex].value;
    var event = event_select.options[event_select.selectedIndex].value;

    table_div.innerHTML = "";
    var table = document.createElement('table');
    table.setAttribute("class", "table table-striped table-bordered table-hover");

    var table_header = ["Champion", "Competition"];
    var thead = document.createElement('thead');
    thead.setAttribute("class", "thead-dark");
    var head_tr = document.createElement('tr');
    for (var i=0; i< table_header.length; i++) {
        var th = document.createElement('th');
        th.setAttribute("class", "text-center");
        th.setAttribute("scope", "col");
        th.innerHTML = table_header[i];
        head_tr.appendChild(th);
    }
    thead.appendChild(head_tr);
    table.appendChild(thead);

    var labels = ["champion_name", "competition"];
    for (var i=0; i<data[region][event]["champions"].length; i++){
        var tr = document.createElement('tr');

        var name_td = document.createElement('td');
        name_td.setAttribute("class", "text-center");
        name_td.innerHTML = '<a href="https://www.worldcubeassociation.org/persons/'+data[region][event]["champions"][i]["champion_id"]+'">'+data[region][event]["champions"][i]["champion_name"]+'</a>';
        tr.appendChild(name_td);

        var competition_td = document.createElement('td');
        competition_td.setAttribute("class", "text-center");
        competition_td.innerHTML = '<a href="https://www.worldcubeassociation.org/competitions/'+data[region][event]["champions"][i]["competition"]+'">'+data[region][event]["champions"][i]["competition"]+'</a>';
        tr.appendChild(competition_td);

        table.appendChild(tr);

        table.appendChild(tr);
    }
    table_div.appendChild(table);

    updateQueryParameter("event", event);

}

var table_div = document.createElement('div')
container.appendChild(table_div);

document.getElementById("content").appendChild(container);

var first_region = getParameterByName("region");
var first_event = getParameterByName("event");

changeEvents();

setSelectValue(select, first_region);
setSelectValue(event_select, first_event);

updateSelectParameter(select, "region");
updateSelectParameter(event_select, "event");
