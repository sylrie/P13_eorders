
function displayElt(id) {

    var elt = document.getElementById(id);
    
    if (elt.style.display === "none") {
        elt.style.display = "block";
    } else {
        elt.style.display = "none";
    }
  }

