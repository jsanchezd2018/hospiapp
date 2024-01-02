const currentDate = new Date();
var today = ("0"+currentDate.getDate()).slice(-2) + "/" + ("0"+(currentDate.getMonth()+1)).slice(-2) + "/" + currentDate.getFullYear();
var now = ("0"+currentDate.getDate()).slice(-2) + "/" + ("0"+(currentDate.getMonth()+1)).slice(-2) + "/" + currentDate.getFullYear()
+ " " + ("0"+currentDate.getHours()).slice(-2) + ":" + ("0"+currentDate.getMinutes()).slice(-2);

document.querySelectorAll('.date').forEach(date => {
    if (date.getAttribute('value') == '' || date.getAttribute('value') == null) {
        date.setAttribute('value', today);
    }
});

document.querySelectorAll('.datetime').forEach(datetime => {
    if (datetime.getAttribute('value') == '' || datetime.getAttribute('value') == null) {
        datetime.setAttribute('value', now);
    }
});