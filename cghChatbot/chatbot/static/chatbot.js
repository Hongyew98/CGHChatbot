function get(selector, root=document) {
    return root.querySelector(selector);
}
function getTime(date) {
    const h = "0" + date.getHours();
    const m = "0" + date.getMinutes();
    return `${h.slice(-2)}:${m.slice(-2)}`;
}
var dt = new Date();
document.getElementById("datetime").innerHTML = (("0"+dt.getHours()).slice(-2)) +":"+ (("0"+dt.getMinutes()).slice(-2));