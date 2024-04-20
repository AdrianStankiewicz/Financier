document.addEventListener('DOMContentLoaded', function () {
    // Switches
    const real = document.getElementById("Real");
    const wdym = document.getElementById("WDYM");

    // Boxes to show or hide
    const realBox = document.getElementById("RealBox");
    const wdymBox = document.getElementById("WDYMBox");
    const ctryBox = document.getElementById("CtryBox");
    const resultBox = document.getElementById("result");

    // Containers for Switches
    const realContainer = document.getElementById("RealContainer");
    const wdymContainer = document.getElementById("WDYMContainer");

    // WDYM inputs
    const wdymAmount = document.getElementById("qtyPrognosis");
    const wdymYears = document.getElementById("years");
    const wdymInflation = document.getElementById("inflation");


    // Switch Controller 
    real.addEventListener('click', function () {
        if (wdymContainer.classList.contains("bg-gray-500")) {
            realContainer.classList.toggle("bg-gray-500");
            wdymContainer.classList.toggle("bg-gray-500");
            real.classList.toggle("font-bold");
            wdym.classList.toggle("font-bold");
            real.classList.toggle("text-white");
            wdym.classList.toggle("text-white");

            realBox.classList.toggle("invisible");
            wdymBox.classList.toggle("invisible");
            ctryBox.classList.toggle("invisible");

            resultBox.textContent = '';

            // clear wdym inputs
            wdymAmount.value = '';
            wdymYears.value = '';
            wdymInflation.value = '';
        }
    });

    wdym.addEventListener('click', function () {
        if (realContainer.classList.contains("bg-gray-500")) {
            realContainer.classList.toggle("bg-gray-500");
            wdymContainer.classList.toggle("bg-gray-500");
            real.classList.toggle("font-bold");
            wdym.classList.toggle("font-bold");
            real.classList.toggle("text-white");
            wdym.classList.toggle("text-white");

            realBox.classList.toggle("invisible");
            wdymBox.classList.toggle("invisible");
            ctryBox.classList.toggle("invisible");

            realBox.style.display = "none";
            resultBox.textContent = '';

            document.getElementById("realForm").reset();
            document.getElementById('flagDiv').innerHTML = '';
        }
    });

    document.getElementById("countryChooser").addEventListener('change', function () {
        realBox.style.display = "flex";

        flagString  = '<img src="images/flags/';
        flagString += document.getElementById("countryChooser").value;
        flagString += '.png" alt="">';
        document.getElementById('flagDiv').innerHTML = flagString;
    });

    document.getElementById("wdymCalculationButton").addEventListener('click', function () {
        let wdymAmountParsed = parseFloat(wdymAmount.value);
        let wdymYearsParsed = parseInt(wdymYears.value);
        let wdymInflationParsed = parseFloat(wdymInflation.value);

        result = '';
        isCorrect = true;

        if (wdymAmount.value == '') isCorrect = false;
        else if (wdymYears.value == '') isCorrect = false;
        else if (wdymInflation.value == '') isCorrect = false;

        if (!isCorrect)
            resultBox.innerHTML = "<span class=\"text-xl text-red-600\">" + 'Due to missing data input(s), the result cannot be calculated' + "</span>";
        else {
            let resultValue = wdymAmountParsed;
            for (let year = 0; wdymYearsParsed > year; year++)
                resultValue *= (100 - wdymInflationParsed) / 100;

            result += "<span class=\"text-md\">The resulting value of the initial ";
            result += "<span class=\"text-xl font-semibold\">amount of " + wdymAmountParsed + "</span>";
            result += " after accounting for the average yearly ";
            result += "<span class=\"text-xl font-semibold\">inflation of " + wdymInflationParsed + "%</span>";
            result += " over the span of ";
            result += "<span class=\"text-xl font-semibold\">" + wdymYearsParsed + " years</span>";
            result += " would be ";
            result += "<span class=\"text-3xl font-semibold\">" + resultValue.toFixed(2) + "</span></span>";
    
            resultBox.innerHTML = result;
        }
    })
});