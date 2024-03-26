document.addEventListener('DOMContentLoaded', function() {
    const real = document.getElementById("Real");
    const wdym = document.getElementById("WDYM");

    const realBox = document.getElementById("RealBox");
    const wdymBox = document.getElementById("WDYMBox");
    const ctryBox = document.getElementById("CtryBox");

    const realContainer = document.getElementById("RealContainer");
    const wdymContainer = document.getElementById("WDYMContainer");

    real.addEventListener('click', function() {
        if(wdymContainer.classList.contains("active")) {
            realContainer.classList.toggle("active");
            wdymContainer.classList.toggle("active");

            realBox.classList.toggle("invisible")
            wdymBox.classList.toggle("invisible")
            ctryBox.classList.toggle("invisible")
        }
    });

    wdym.addEventListener('click', function() {
        if(realContainer.classList.contains("active")) {
            realContainer.classList.toggle("active");
            wdymContainer.classList.toggle("active");
            
            realBox.classList.toggle("invisible")
            wdymBox.classList.toggle("invisible")
            ctryBox.classList.toggle("invisible")

            realBox.style.display = "none";
        }
    });

    document.getElementById("countryChooser").addEventListener('change', function() {
        realBox.style.display = "flex";
    });
});