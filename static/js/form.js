function validate() {
    var sequence = document.forms["userInput"]["userSequence"]
    var errorMessage = "";
    var error = document.querySelector('.error');

    if (sequence.value == ""){
        errorMessage += " You didn't enter any numbers!";
        sequence.focus();
        return false;
    }
    sequence.value = sequence.value.replace(/^\s+|\s+$/g,''); 
    var seqArray = sequence.value.split(" ");
    var negative = false;
    var increasing = false;
    var notInteger = false;
    var  er = /^-?[0-9]+$/;
    var secNumber = false;
    if (seqArray[0] == seqArray[1]) {
        secNumber = true;
    }

    for (var i = 0; i < seqArray.length - 1; i++){
        var value = Number(seqArray[i]);
        if (value < 0) {
            negative = true;
        }
        var nextValue = Number(seqArray[i+1]);
        if (value < nextValue) {
            increasing = true;
        }
        var isInt = er.test(seqArray[i]);
        if (!isInt)  {
            notInteger = true;
        }
    }
    if (seqArray[0] != seqArray.length - 1) {
        errorMessage += " The number of elements doesn't match the first number.";
    }

    if (negative) {
        errorMessage += " All numbers should be non-negative.";
    }

    if (increasing){
        errorMessage += " The sequence should be non-increasing.";
    }

    if (notInteger) {
        errorMessage += " All numbers should be integers.";
    }

    if (secNumber){
        errorMessage += " Second Number is too high."
    }

    if (errorMessage != "") {
        error.innerHTML = errorMessage;
        error.className = "error active";
        return false;
    }
    else {
        error.innerHTML = ""; // Reset the content of the message
        error.className = "error";
    }

    return true;

}
