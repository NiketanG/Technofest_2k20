window.onload = function load() {
    NavBarPos();
    //Preloader
    function hidePreloader() {
        $('.loader').fadeOut(500);
    }

    setTimeout(() => {
        hidePreloader();
    }, 1000);
}

function loadform() {
    selectlist();
    setgrp();
    event_check();
}

function selectlist() {
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
            c.addEventListener("click", function (e) {
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
        a.addEventListener("click", function (e) {
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

window.onscroll = function () {
    NavBarPos();
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
    if (Math.max(document.body.scrollTop, window.pageYOffset) >= 60) {
        document.getElementsByClassName("menu")[0].classList.add("sticky");
        document.getElementsByClassName("logo")[0].style.lineHeight = "40px";
        document.getElementsByClassName("logo")[0].style.fontSize = "20px";
        document.getElementById("totop").style.display = "block";
        $("ul").css("background-color", "black");
        $("ul").css("color", "white");
    } else {
        document.getElementById("nav").classList.remove("sticky");
        document.getElementsByClassName("logo")[0].style.lineHeight = "80px";
        document.getElementsByClassName("logo")[0].style.fontSize = "25px";
        document.getElementById("totop").style.display = "none";

        if (($(".item").hasClass("active"))) {
            document.getElementsByClassName("navbar")[0].style.paddingBottom = "145px";
            $("ul").css("background-color", "black");
            $("ul").css("color", "white");
        } else {
            document.getElementsByClassName("navbar")[0].style.paddingBottom = "25px";
            $("ul").css("background-color", "transparent");
            $("ul").css("color", "black");
        }

    }
}


function toggle() {
    if ($(".item").hasClass("active")) {
        $(".item").removeClass("active");
        $(".menu").find("div").html("<i class='fas fa-bars'></i>");
        if (Math.max(document.body.scrollTop, window.pageYOffset) <= 60) {
            $("ul").css("background-color", "transparent");
            $("ul").css("color", "black");
            document.getElementsByClassName("navbar")[0].style.paddingBottom = "25px";
        }
    } else {
        $(".item").addClass("active");
        $(".menu").find("div").html("<i class='fas fa-times'></i>");
        if (Math.max(document.body.scrollTop, window.pageYOffset) <= 60) {
            $("ul").css("background-color", "black");
            $("ul").css("color", "white");
            document.getElementsByClassName("navbar")[0].style.paddingBottom = "145px";
        }
    }
}

function validate_name() {
    var name = document.getElementById("name").value;
    var re_name = /^[A-Za-z ]/;
    if (name.length < 1) {
        document.getElementById("name_vb").style.display = 'block';
        return false;
    } else if ((name.length > 0) && ((re_name.test(name) == false))) {
        document.getElementById("name_v").style.display = 'block';
        document.getElementById("name_vb").style.display = 'none';
        return false;
    } else if ((re_name.test(name)) || (name.length < 1)) {
        document.getElementById("name_v").style.display = 'none';
        document.getElementById("name_vb").style.display = 'none';
        return true;
    }
}

function validate_email() {
    blank_check();
    var email = document.getElementById("email").value;
    var re_email = /(^\w)*[@](\w)*(\.)(\w)*/;
    if (email.length < 1) {
        document.getElementById("email_vb").style.display = 'block';
        return false;
    } else if ((email.length > 0) && ((re_email.test(email) == false))) {
        document.getElementById("email_v").style.display = 'block';
        document.getElementById("email_vb").style.display = 'none';
        return false;
    } else if ((re_email.test(email)) || (email.length < 1)) {
        document.getElementById("email_v").style.display = 'none';
        document.getElementById("email_vb").style.display = 'none';
        return true;
    }
}

function validate_phno() {
    blank_check();
    var phno = document.getElementById("PhNo").value;
    var re_phno = /^\d{10}$/;
    if (phno.length < 1) {
        document.getElementById("phone_vb").style.display = 'block';
        return false;
    } else if ((phno.length > 0) && ((re_phno.test(phno) == false))) {
        document.getElementById("phone_v").style.display = 'block';
        document.getElementById("phone_vb").style.display = 'none';
        return false;
    } else if ((re_phno.test(phno)) || (phno.length < 1)) {
        document.getElementById("phone_v").style.display = 'none';
        document.getElementById("phone_vb").style.display = 'none';
        return true;
    }
}

function validate_clg() {
    blank_check();
    var clgname = document.getElementById("ClgName").value;
    if (clgname.length < 1) {
        document.getElementById("clg_vb").style.display = 'block';
        return false;
    } else if (clgname.length > 0) {
        document.getElementById("clg_vb").style.display = 'none';
        return true;
    }
}

function setgrp() {
    var checkedrdbtn = document.querySelector('input[name="radio_team"]:checked').value;

    if (checkedrdbtn == "solo") {
        for (let el of document.querySelectorAll('.grp')) el.style.display = 'none';
        document.getElementById("GrpName").disabled = true;

    } else {
        for (let el of document.querySelectorAll('.grp')) el.style.display = 'block';
        document.getElementById("GrpName").disabled = false;
    }
}

function validate_grp() {
    blank_check();
    var checkedrdbtn = document.querySelector('input[name="radio_team"]:checked').value;

    if (checkedrdbtn == "solo") {
        return true;
    } else {
        var grpname = document.getElementById("GrpName").value;
        if (grpname.length < 1) {
            document.getElementById("group_vb").style.display = 'block';
            return false;
        } else if (grpname.length > 0) {
            document.getElementById("group_vb").style.display = 'none';
            return true;
        }
    }
}

//Blank Check
function blank_check() {
    var x = document.forms["Register"].value;
    var checkedrdbtn = document.querySelector('input[name="radio_team"]:checked').value;

    if ((x == "") && (checkedrdbtn == "solo")) {
        document.getElementById("registerbtn").disabled = true;
        return false;
    } else {
        document.getElementById("registerbtn").disabled = false;
        return true;
    }
}

function event_check() {
    var e = document.getElementById("events").selectedIndex;
    if ((e == '0')) {
        document.getElementById("registerbtn").disabled = true;
        return false;
    } else {
        document.getElementById("registerbtn").disabled = false;
        return true;
    }
}

function validate() {
    if (validate_name() && event_check() && validate_phno() && validate_email() && validate_clg() && validate_grp() && blank_check()) {
        //Submit Form 
        document.getElementsByTagName("form")[0].submit();
        alert("Registration Successful ! :)")
    } else {
        alert("Please check all fields.")
    }
}

function scrolltoelement(element) {
    var element = document.getElementById("element");
    element.scrollIntoView();
}

function event_desc(event_id) {
    if ($(".event_desc_text:nth-child(" + event_id + ")").is(':hidden')) {
        $(".event_desc").fadeIn("slow");
        $(".event_desc_text").hide();
        $(".event_desc_text:nth-child(" + event_id + ")").show("500");
        $(".active_event").hide();
        $("#event_" + event_id).fadeIn("500");

    } else {
        $(".event_desc_text:nth-child(" + event_id + ")").hide("fast");
        $(".event_desc").hide();
        $(".active_event").hide();
    }
}