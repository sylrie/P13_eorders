
function displayElt(id, idButton) {

    var elt = document.getElementById(id);
    var button = document.getElementById(idButton)

    if (elt.style.display === "none") {
        elt.style.display = "block";
        if (idButton){
            button.style.border = 'solid #f14806';
        }
        

        
    } else {
        elt.style.display = "none";
        if (idButton){
            button.style.border = 'None';
        }
    }
  }

function Payment(amount, type) {
    if (type == 'cb'){
        alert("Un paiement de " + amount + "€ à été effectué par CB")
    } else {
        alert("Un memre de l'équipe à été prévenue, vous devrez régler " + amount + "€")
    }
    
}