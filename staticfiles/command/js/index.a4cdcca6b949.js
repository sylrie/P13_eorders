
function displayElt(id) {

    var elt = document.getElementById(id);
    
    if (elt.style.display === "none") {
        elt.style.display = "block";
    } else {
        elt.style.display = "none";
    }
  }

function Payment(amount, type) {
    if (type == 'cb'){
        alert("Un paiement de " + amount + "€ à été effectué par CB")
    } else {
        alert("Un memre de l'équipe à été prévenue, vous devrez régler " + amount + "€")
    }
    
}