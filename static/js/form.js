function validate(){
var sequence = document.forms["userInput"]["userSequence"]

if (sequence.value == ""){
  window.alert("you didn't enter any numbers");
  sequence.focus();
  return false;
}

var seqArray = sequence.value.split(" ");
var errorMessage = "";
var negative = false;
var increasing = false;

for (i = 0; i < seqArray.length - 1; i++){
  var value = Number(seqArray[i]);
  if (value < 0) {
    negative = true;
  }
  var nextValue = Number(seqArray[i+1]);
  if (value < nextValue) {
    increasing = true;
  }
}
if (seqArray[0] != seqArray.length - 1) {
  errorMessage += " The number of elements doesn't match the first number."
}

if (negative) {
  errorMessage += " The numbers should be non-negative.";
}

if (increasing){
  errorMessage += " The sequence should be non-increasing."
}

if (errorMessage != "") {
  window.alert(errorMessage);
  return false;
}

return true;

}
