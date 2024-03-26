function updateFormAction() {
    var selectedCurrency = document.getElementById("currency_id").value;
    document.getElementById("currencyForm").setAttribute("hx-get", "/currency_history_check/" + selectedCurrency);
}