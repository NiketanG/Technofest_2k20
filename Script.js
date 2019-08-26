window.onload = function() {
    selectlist();
    setgrp();
}

function selectlist(){
var x, i, j, selElmnt, a, b, c;
/*look for any elements with the class "custom-select":*/
x = document.getElementsByClassName("custom-select");
for (i = 0; i < x.length; i++) {
  selElmnt = x[i].getElementsByTagName("select")[0];
  /*for each element, create a new DIV that will act as the selected item:*/
  a = document.createElement("DIV");
  a.setAttribute("class", "select-selected");
  a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
  x[i].appendChild(a);
  /*for each element, create a new DIV that will contain the option list:*/
  b = document.createElement("DIV");
  b.setAttribute("class", "select-items select-hide");
  for (j = 1; j < selElmnt.length; j++) {
    /*for each option in the original select element,
    create a new DIV that will act as an option item:*/
    c = document.createElement("DIV");
    c.innerHTML = selElmnt.options[j].innerHTML;
    c.addEventListener("click", function(e) {
        /*when an item is clicked, update the original select box,
        and the selected item:*/
        var y, i, k, s, h;
        s = this.parentNode.parentNode.getElementsByTagName("select")[0];
        h = this.parentNode.previousSibling;
        for (i = 0; i < s.length; i++) {
          if (s.options[i].innerHTML == this.innerHTML) {
            s.selectedIndex = i;
            h.innerHTML = this.innerHTML;
            y = this.parentNode.getElementsByClassName("same-as-selected");
            for (k = 0; k < y.length; k++) {
              y[k].removeAttribute("class");
            }
            this.setAttribute("class", "same-as-selected");
            break;
          }
        }
        h.click();
    });
    b.appendChild(c);
  }
  x[i].appendChild(b);
  a.addEventListener("click", function(e) {
      /*when the select box is clicked, close any other select boxes,
      and open/close the current select box:*/
      e.stopPropagation();
      closeAllSelect(this);
      this.nextSibling.classList.toggle("select-hide");
      this.classList.toggle("select-arrow-active");
    });
}
}
function closeAllSelect(elmnt) {
  /*a function that will close all select boxes in the document,
  except the current select box:*/
  var x, y, i, arrNo = [];
  x = document.getElementsByClassName("select-items");
  y = document.getElementsByClassName("select-selected");
  for (i = 0; i < y.length; i++) {
    if (elmnt == y[i]) {
      arrNo.push(i)
    } else {
      y[i].classList.remove("select-arrow-active");
    }
  }
  for (i = 0; i < x.length; i++) {
    if (arrNo.indexOf(i)) {
      x[i].classList.add("select-hide");
    }
  }
}
/*if the user clicks anywhere outside the select box,
then close all select boxes:*/
document.addEventListener("click", closeAllSelect);

window.onscroll = function() {
    NavBarPos();
}

function getCookie(name) {
    var dc = document.cookie;
    var prefix = name + "=";
    var begin = dc.indexOf("; " + prefix);
    if (begin == -1) {
        begin = dc.indexOf(prefix);
        if (begin != 0) return null;
    }
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

function NavBarResize() {
    var x = document.getElementById("topnav");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
}

function NavBarPos() {
    if (Math.max(document.body.scrollTop,window.pageYOffset) >= 60) {
        document.getElementById("topnav").classList.add("sticky");
        document.getElementById("totop").style.display = "block";
        document.getElementById("topnav").style.padding = "0px 10px";
        document.getElementById("title").style.fontSize = "16px";
        document.getElementById("title").style.paddingTop = "20px";
    } else {
        document.getElementById("topnav").classList.remove("sticky");
        document.getElementById("totop").style.display = "none";
        document.getElementById("topnav").style.padding = "20px 10px";
        document.getElementById("title").style.fontSize = "30px";
        document.getElementById("title").style.paddingTop = "10px";
    }
}

function validate_form() {
    var email= document.getElementById("email").value;
    var name=document.getElementById("name").value;
    var grpname=document.getElementById("GrpName").value;
    var clgname=document.getElementById("ClgName").value;
    var phno=document.getElementById("PhNo").value;
    
    var re_email = /(^\w)*[@](\w)*(\.)(\w)*/;
    var re_name = /((^\w)*)/
    var re_phno= /^\d{10}$/;

    if (email.length < 1) {
        document.getElementById("email_vb").style.display = 'block';
    } else if ((email.length > 0) && ((re_email.test(email) == false))) {
        document.getElementById("email_v").style.display = 'block';
        document.getElementById("email_vb").style.display = 'none';
    }
    else if ((re_email.test(email)) || (email.length < 1)) {
        document.getElementById("email_v").style.display = 'none'; 
        document.getElementById("email_vb").style.display = 'none';
    }

    if (phno.length < 1) {
        document.getElementById("phone_vb").style.display = 'block';
    } else if ((phno.length > 0) && ((re_phno.test(phno) == false))) {
        document.getElementById("phone_v").style.display = 'block';
        document.getElementById("phone_vb").style.display = 'none';
    }
    else if ((re_phno.test(phno)) || (phno.length < 1)) {
        document.getElementById("phone_v").style.display = 'none'; 
        document.getElementById("phone_vb").style.display = 'none';
    } 

    if (name.length < 1) {
        document.getElementById("name_vb").style.display = 'block';
    } else if (name.length > 0) {
        document.getElementById("name_vb").style.display = 'none';
    }

    if (clgname.length < 1) {
        document.getElementById("clg_vb").style.display = 'block';
    } else if (clgname.length > 0) {
        document.getElementById("clg_vb").style.display = 'none';
    }

    if (grpname.length < 1) {
        document.getElementById("group_vb").style.display = 'block';
    } else if (grpname.length > 0) {
        document.getElementById("group_vb").style.display = 'none';
    }
    setgrp();
}

function setgrp(){
    var checkedrdbtn = document.querySelector('input[name="radio_team"]:checked').value;
    
    if(checkedrdbtn == "solo" ) {
        for (let el of document.querySelectorAll('.grp')) el.style.display = 'none';
    } else {
        for (let el of document.querySelectorAll('.grp')) el.style.display = 'block';
    }
}


