document.addEventListener("DOMContentLoaded", function() {
    var slider = document.getElementById("slider");
    var output = document.getElementById("output");
    output.innerHTML = slider.value;
  
    slider.oninput = function() {
      output.innerHTML = this.value / 100;
    }
});
  
document.addEventListener('DOMContentLoaded', function () {
    var incrementButton = document.getElementById('increment-button');
    var decrementButton = document.getElementById('decrement-button');
    var quantityInput = document.getElementById('quantity-input');

    incrementButton.addEventListener('click', function () {
        quantityInput.value = parseInt(quantityInput.value) + 10000;
    });

    decrementButton.addEventListener('click', function () {
        var result = parseInt(quantityInput.value) - 10000;
        
        if(result < 0)
            quantityInput.value = 0;
        else
            quantityInput.value = result;

    });
});