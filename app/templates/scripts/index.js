function handleImageHover(element, animatedSrc, staticSrc) {
    element.addEventListener("mouseenter", function() {
        element.src = animatedSrc;
    });

    element.addEventListener("mouseleave", function() {
        element.src = staticSrc;
    });
}

document.addEventListener("DOMContentLoaded", function() {

    handleImageHover(
        document.getElementById("calculator"), 
        "animations/calculator.gif", 
        "images/calculator.png"
        );

    handleImageHover(
        document.getElementById("question"), 
        "animations/question.gif", 
        "images/question.png"
        );

    handleImageHover(
        document.getElementById("exchange"), 
        "animations/exchange.gif", 
        "images/exchange.png"
    );

    handleImageHover(
        document.getElementById("list"), 
        "animations/list.gif", 
        "images/list.png"
    );

    handleImageHover(
        document.getElementById("history"), 
        "animations/history.gif", 
        "images/history.png"
    );

    handleImageHover(
        document.getElementById("inflation"), 
        "animations/inflation.gif", 
        "images/inflation.png"
    );

});