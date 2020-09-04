function displayManager(id, idButton) {
    const eltList = [
        'others',
        'Tapas',
        'Plats',
        'Boisson chaudes',
        'Softs',
        'Bières',
        'Vins'
    ]

    eltList.forEach(function(item) {
        console.log(item)
        
        var elt = document.getElementById(item);
        var buttonName = item+'button'
        var button = document.getElementById(buttonName)

        if (elt.style.display === "block") {
            elt.style.display = "none";
            button.style.border = 'None';
        }    
        else {}
    })
    displayElt(id, idButton)
}

function displayElt(id, idButton) {

    var elt = document.getElementById(id);
    var button = document.getElementById(idButton)

    if (elt.style.display === "none") {
        elt.style.display = "block";
        if (idButton){
            button.style.border = 'solid #f14806';
        }
        elt.scrollIntoView({block: "end"});
        
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