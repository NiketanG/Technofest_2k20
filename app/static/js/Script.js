window.onload = function load() {
    this.set_counter();
    //Preloader 
    setTimeout(() => {
        $('.loader').fadeOut(500);
    }, 100);
};

window.onscroll = function () {
    NavBarPos();
};

$.fn.isInViewport = function() {
    var elementTop = $(this).offset().top;
    var elementBottom = elementTop + $(this).outerHeight();
  
    var viewportTop = $(window).scrollTop();
    var viewportBottom = viewportTop + $(window).height();
  
    return elementBottom > viewportTop && elementTop < viewportBottom;
};

function NavBarPos() {
    if (Math.max(document.body.scrollTop, window.pageYOffset) >= 60) {
        $(".menu").addClass("sticky");
        $(".logo").css({
            "lineHeight": "40px",
            "fontSize": "20px"
        });
        $("#totop").show();
        $("ul").css({
            "background-color": "black",
            "color": "white"
        });
        $(".toggle").css("filter", "invert(0)");
        $("ul").mouseleave(function () {
            $(".toggle").css("filter", "invert(0)");
        });
    } else {
        $(".toggle").css("filter", "invert(1)");
        $("ul").mouseleave(function () {
            $(".toggle").css("filter", "invert(1)");
        });
        $(".menu").removeClass("sticky");
        $(".logo").css({
            "lineHeight": "80px",
            "fontSize": "25px"
        });
        $("#totop").hide();
        if (($(".item").hasClass("active"))) {
            //$(".navbar").css("paddingBottom", "145px");
            $("ul").css({
                "background-color": "black",
                "color": "white"
            });
        } else {
            //$(".navbar").css("paddingBottom", "25px");
            $("ul").css({
                "background-color": "transparent",
                "color": "black"
            });
        }
    }
}

function toggle() {
    if ($(".item").hasClass("active")) {
        $(".item").removeClass("active");
        $(".menu .toggle img").toggle();
        if (Math.max(document.body.scrollTop, window.pageYOffset) <= 60) {
            $("ul").css({
                "background-color": "transparent",
                "color": "black"
            });
            $(".toggle").css("filter", "invert(1)");
            //$(".navbar").css("paddingBottom", "25px");
        }
    } else {
        $(".item").addClass("active");
        $(".menu .toggle img").toggle();
        if (Math.max(document.body.scrollTop, window.pageYOffset) <= 60) {
            $("ul").css({
                "background-color": "black",
                "color": "white"
            });
            $(".toggle").css("filter", "invert(0)");
            //$(".navbar").css("paddingBottom", "145px");
        }
    }
}

// Set the date we're counting down to
var countDownDate = new Date("Jan 17, 2020 09:30:00").getTime();
// Get today's date and time
var now = new Date().getTime();

function set_counter() {
    // Find the distance between now and the count down date
    var distance = countDownDate - now;
    // Time calculations for months, days, hours
    var months = Math.floor(distance / (1000 * 60 * 60 * 24 * 30));
    var days = Math.floor((distance % (1000 * 60 * 60 * 24 * 30)) / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    $(".months h2").html(months);
    $(".days h2").html(days);
    $(".hours h2").html(hours);
    // If the count down is finished, write some text
    if (distance < 0) {
        clearInterval(x);
    }
}
// Update the count down every 1 minute
setInterval(set_counter, 1000);

$(document).ready(function () {
    $("ul").hover(function () {
        $(".toggle").css("filter", "invert(0)");
    }, function () {
        $(".toggle").css("filter", "invert(1)");
    });
});

