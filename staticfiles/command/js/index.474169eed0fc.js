function displayManager(id, idButton) {
    
    const eltList = [
        'others',
        'Tapas',
        'Plats',
        'Boissons chaudes',
        'Softs',
        'Bières',
        'Vins'
    ]

    eltList.forEach(function(item) {
        
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

function loadingGif(){
    
    let elt = $("#loading")[0];
    
      
    var newA = elt.appendChild(document.createElement("a"));
    newA.id ="searching";

    var newImg = newA.appendChild(document.createElement("img"));
    newImg.src = "../static/command/img/loader.gif";
    newImg.setAttribute("style", "max-height:70px;")
    elt.scrollIntoView();
  };