document.addEventListener('DOMContentLoaded', function () {
    const formTotal = document.getElementById('formTotal')
    const formLength = document.getElementById('formLength')
    const formInstallments = document.getElementById('formInstallments')

    const outputFinal = document.getElementById('outputFinal');

    let item = ''

    document.querySelectorAll('input[name="optionCalculator"]').forEach((elem) => {
        elem.addEventListener("change", function (event) {
            item = event.target.value;

            outputFinal.innerHTML = '';

            if (item == 'total') {
                if (formTotal.classList.contains('hidden')) {
                    formTotal.classList.remove('hidden');
                    formLength.classList.add('hidden');
                    formInstallments.classList.add('hidden');
                }
            }
            else if (item == 'length') {
                if (formLength.classList.contains('hidden')) {
                    formTotal.classList.add('hidden');
                    formLength.classList.remove('hidden');
                    formInstallments.classList.add('hidden');
                }
            }
            else if (item == 'installments') {
                if (formInstallments.classList.contains('hidden')) {
                    formTotal.classList.add('hidden');
                    formLength.classList.add('hidden');
                    formInstallments.classList.remove('hidden');
                }
            }
        });
    });

    const incrementButtonTotal = document.getElementById('increment-button-total');
    const decrementButtonTotal = document.getElementById('decrement-button-total');
    const quantityInputTotal = document.getElementById('quantity-input-total');

    incrementButtonTotal.addEventListener('click', function () {
        if (isEmpty(quantityInputTotal.value)) {
            quantityInputTotal.value = 10000;
        }
        else {
            quantityInputTotal.value = parseInt(quantityInputTotal.value) + 10000;
        }
    });

    decrementButtonTotal.addEventListener('click', function () {
        if (isEmpty(quantityInputTotal.value)) {
            quantityInputTotal.value = 0;
        }
        else if (parseInt(quantityInputTotal.value) - 10000 < 0)
            quantityInputTotal.value = 0;
        else
            quantityInputTotal.value = parseInt(quantityInputTotal.value) - 10000;
    });

    const incrementButtonLength = document.getElementById('increment-button-length');
    const decrementButtonLength = document.getElementById('decrement-button-length');
    const quantityInputLength = document.getElementById('quantity-input-length');

    incrementButtonLength.addEventListener('click', function () {
        if (isEmpty(quantityInputLength.value)) {
            quantityInputLength.value = 10000;
        }
        else {
            quantityInputLength.value = parseInt(quantityInputLength.value) + 10000;
        }
    });

    decrementButtonLength.addEventListener('click', function () {
        if (isEmpty(quantityInputLength.value)) {
            quantityInputLength.value = 0;
        }
        else if (parseInt(quantityInputLength.value) - 10000 < 0)
            quantityInputLength.value = 0;
        else
            quantityInputLength.value = parseInt(quantityInputLength.value) - 10000;
    });

    const incrementButtonInstallments = document.getElementById('increment-button-installments');
    const decrementButtonInstallments = document.getElementById('decrement-button-installments');
    const quantityInputInstallments = document.getElementById('quantity-input-installments');

    incrementButtonInstallments.addEventListener('click', function () {
        if (isEmpty(quantityInputInstallments.value)) {
            quantityInputInstallments.value = 10000;
        }
        else {
            quantityInputInstallments.value = parseInt(quantityInputInstallments.value) + 10000;
        }
    });

    decrementButtonInstallments.addEventListener('click', function () {
        if (isEmpty(quantityInputInstallments.value)) {
            quantityInputInstallments.value = 0;
        }
        else if (parseInt(quantityInputInstallments.value) - 10000 < 0)
            quantityInputInstallments.value = 0;
        else
            quantityInputInstallments.value = parseInt(quantityInputInstallments.value) - 10000;
    });
});

function isEmpty(str) {
    return !str.trim().length;
}

// slider JS
document.addEventListener("DOMContentLoaded", function () {
    const sliderTotal = document.getElementById("sliderTotal");
    const outputTotal = document.getElementById("outputTotal");

    sliderTotal.oninput = function () {
        outputTotal.innerHTML = this.value / 100;
    }
    outputTotal.innerHTML = sliderTotal.value;

    const sliderLength = document.getElementById("sliderLength");
    const outputLength = document.getElementById("outputLength");
    sliderLength.oninput = function () {
        outputLength.innerHTML = this.value / 100;
    }
    outputLength.innerHTML = sliderLength.value;

    const sliderInstallments = document.getElementById("sliderInstallments");
    const outputInstallments = document.getElementById("outputInstallments");
    sliderInstallments.oninput = function () {
        outputInstallments.innerHTML = this.value / 100;
    }
    outputInstallments.innerHTML = sliderInstallments.value;
});

document.addEventListener("DOMContentLoaded", function () {
    const buttonTotal = document.getElementById('buttonTotal');
    const buttonLength = document.getElementById('buttonLength');
    const buttonInstallments = document.getElementById('buttonInstallments');

    const outputFinal = document.getElementById('outputFinal');

    const inputAmmountTotal = document.getElementById('quantity-input-total');
    const inputLengthTotal = document.getElementById('lengthTotal');
    const sliderTotal = document.getElementById("outputTotal");

    const inputAmmountLength = document.getElementById('quantity-input-length');
    const inputInstallmentsLength = document.getElementById('installmentsLength');
    const sliderLength = document.getElementById("outputLength");

    const inputAmmountInstallments = document.getElementById('quantity-input-installments');
    const inputLengthInstallments = document.getElementById('lengthInstallments');
    const sliderInstallments = document.getElementById("outputInstallments");

    // --------------------------------------------------------------------
    // ## Variables guide:
    // 
    // pv = present value       ->  ammount borrowed
    // nper = number of periods ->  how many periods will occur
    // rate = interest rate     ->  interest rate per period
    // fv = future value        ->  ammount to be finally repaid
    // 
    // 
    // Calculate the total ammount of money that will have to be repaid 
    buttonTotal.addEventListener('click', function () {
        let pv = parseFloat(inputAmmountTotal.value);
        let nper = parseInt(inputLengthTotal.value);
        let rate = parseFloat(sliderTotal.innerText) / 12;
        let fv = pv * (1 + rate) ^ nper;

        outputFinal.innerHTML = '\
            <div class="w-5/6">\
                <div class="flex flex-col mt-5">\
                    <span class="text-md">Total value to be repaid:</span>\
                    <span class="text-4xl">' + fv + '$</span>\
                </div>\
                <div class="flex flex-col mt-5">\
                    <hr class="mb-2">\
                    <span class="text-md">Cost of the loan:</span>\
                    <span class="text-4xl">'+ (fv - pv) +'$</span>\
                </div>\
                <div class="mt-10">\
                    <hr class="mb-2">\
                    <span class="text-sm mt-5 text-gray-500">The amount of installments or total value quoted may not include other fees such as additional insurance or commissions that the borrower may have.</span>\
                </div>\
            </div>\
            ';
    });

    // --------------------------------------------------------------------
    // ## Variables guide:
    // 
    // pv = present value       ->  ammount borrowed
    // pmt = regular payment    ->  the payment per period
    // rate = interest rate     ->  interest rate per period
    // nper = number of periods ->  how many periods will occur
    // 
    // 
    // Calculate how many periods will have to occur to pay off the borrowed ammount
    buttonLength.addEventListener('click', function () {
        let pv = parseFloat(inputAmmountLength.value);
        let nper = 0;
        let rate = parseFloat(sliderLength.innerText) / 1200;
        let pmt = parseFloat(inputInstallmentsLength.value);

        let tempPv = pv;
        for(nper = 0; tempPv > 0; nper++) {
            tempPv += tempPv * rate;
            tempPv -= pmt;
        }

        outputFinal.innerHTML = '\
            <div class="w-5/6">\
                <div class="flex flex-col mt-5">\
                    <span class="text-md">Amount of required payments:</span>\
                    <span class="text-4xl">' + nper + '</span>\
                </div>\
                <div class="mt-10">\
                    <hr class="mb-2">\
                    <span class="text-sm mt-5 text-gray-500">The amount of installments or total value quoted may not include other fees such as additional insurance or commissions that the borrower may have.</span>\
                </div>\
            </div>\
            ';
    });

    // --------------------------------------------------------------------
    // ## Variables guide:
    // 
    // pv = present value       ->  ammount borrowed
    // rate = interest rate     ->  interest rate per period
    // nper = number of periods ->  how many periods will occur
    // pmt = regular payment    ->  the payment per period
    // 
    // 
    // Calculate the ammount to pay per period to pay off the borrowed ammount in specified time
    buttonInstallments.addEventListener('click', function () {
        let pv = parseFloat(inputAmmountInstallments.value);
        let rate = parseFloat(sliderInstallments.innerText) / 1200;
        let nper = parseFloat(inputLengthInstallments.value);
        let pmt = 0;

        let numerator = -pv * Math.pow(1 + rate, nper);
        let denominator = Math.pow(1 + rate, nper) - 1;
        pmt = -(numerator * rate / denominator);


        console.log("Payment per period:", pmt );
        
        outputFinal.innerHTML = '\
            <div class="w-5/6">\
                <div class="flex flex-col mt-5">\
                    <span class="text-md">Amount per installment:</span>\
                    <span class="text-4xl">' + pmt + '</span>\
                </div>\
                <div class="mt-10">\
                    <hr class="mb-2">\
                    <span class="text-sm mt-5 text-gray-500">The amount of installments or total value quoted may not include other fees such as additional insurance or commissions that the borrower may have.</span>\
                </div>\
            </div>\
            ';
    });
});