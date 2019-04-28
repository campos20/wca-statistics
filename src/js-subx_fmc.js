import {
  updateSelectParameter,
  getParameterByName,
  setSelectValue,
  updateQueryParameter
} from "./useQueryParameter.js";

var content = document.querySelector("#content");
content.setAttribute("class", "container text-center");

var h2 = document.createElement("h2");
h2.classList.add("text-center");
h2.innerHTML = title;
content.appendChild(h2);

var selectDiv = document.createElement("div");
selectDiv.setAttribute("float", "left");
selectDiv.innerHTML = "Sub ";

var select = document.createElement("select");
select.addEventListener("change", changeMoves);
selectDiv.appendChild(select);

content.appendChild(selectDiv);

Object.keys(data).forEach(moves => {
  var option = document.createElement("option");
  option.innerHTML = moves;
  select.appendChild(option);
});

var table_div = document.createElement("div");
content.appendChild(table_div);

var first_moves = getParameterByName("moves");
if (first_moves !== null) {
  setSelectValue(select, first_moves);
}
changeMoves();
updateSelectParameter(select, "moves");

function changeMoves() {
  var moves = select.options[select.selectedIndex].value;

  table_div.innerHTML = "";
  var table = document.createElement("table");
  table.setAttribute("class", "table table-striped table-bordered table-hover");

  var table_header = ["Pos", "Count", "Competitor", "Country"];
  var thead = document.createElement("thead");
  thead.setAttribute("class", "thead-dark");
  var head_tr = document.createElement("tr");
  for (var i = 0; i < table_header.length; i++) {
    var th = document.createElement("th");
    th.setAttribute("class", "text-center");
    th.setAttribute("scope", "col");
    th.innerHTML = table_header[i];
    head_tr.appendChild(th);
  }
  thead.appendChild(head_tr);
  table.appendChild(thead);

  var tbody = document.createElement("tbody");

  for (var i = 0; i < data[moves].length; i++) {
    var tr = document.createElement("tr");

    var pos_td = document.createElement("td");
    pos_td.innerHTML =
      i > 0 && data[moves][i]["moves"] === data[moves][i - 1]["moves"]
        ? "-"
        : i + 1;
    tr.appendChild(pos_td);

    var moves_td = document.createElement("td");
    moves_td.innerHTML = data[moves][i]["moves"];
    tr.appendChild(moves_td);

    var name_td = document.createElement("td");
    name_td.innerHTML =
      '<a href="https://www.worldcubeassociation.org/persons/' +
      data[moves][i]["competitor_id"] +
      '">' +
      data[moves][i]["name"] +
      "</a>";
    tr.appendChild(name_td);

    var country_td = document.createElement("td");
    country_td.innerHTML = data[moves][i]["country"];
    tr.appendChild(country_td);

    tbody.appendChild(tr);
  }
  table.appendChild(tbody);
  table_div.appendChild(table);

  updateQueryParameter("moves", moves);
}
