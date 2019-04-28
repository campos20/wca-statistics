export function getParameterByName(name) {
  // https://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
  let url = window.location.href;
  name = name.replace(/[\[\]]/g, "\\$&");
  var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
    results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return "";
  return decodeURIComponent(results[2].replace(/\+/g, " "));
}

export function setSelectValue(select, value) {
  for (var i = 0; i < select.length; i++) {
    if (select[i].value === value) {
      select.selectedIndex = i;
      break;
    }
  }
}

export function updateSelectParameter(select, name) {
  var value = select.options[select.selectedIndex].value;
  updateQueryParameter(name, value);
}

export function updateQueryParameter(key, value) {
  let uri = window.location.href;
  let re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
  let separator = uri.indexOf("?") !== -1 ? "&" : "?";
  if (uri.match(re)) {
    uri = uri.replace(re, "$1" + key + "=" + value + "$2");
  } else {
    uri = uri + separator + key + "=" + value;
  }
  window.history.replaceState("", "", uri);
}
