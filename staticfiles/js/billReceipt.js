function printReceipt(){
    let navbar=document.getElementById("navb")
    let container=document.getElementById("cont")
    let print=document.getElementById("print")
    let paybtn=document.getElementById("paybtn")
    let tax=document.getElementById("tax")

    navbar.style.display="none";
    container.style.background="transparent";
    container.style.marginTop="3em";
    print.style.visibility="hidden";
    paybtn.style.visibility="hidden";
    tax.style.fontSize="1.5em";
    window.print()
    navbar.style.display="block";
    container.style.backgroundColor="#f8f9fa";
    container.style.marginTop="8em";
    print.style.visibility="visible";
    paybtn.style.visibility="visible";
    tax.style.fontSize="1.9em";
}