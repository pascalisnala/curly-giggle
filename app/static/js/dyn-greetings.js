var text = ["Meet", "Recontrer", "会う", "Temui", "Tavata", "Conocer a", "만나다"];
var counter = 0;
var elem = document.getElementById("dyn-greetings");
var inst = setInterval(change, 1000);

function change() {
  elem.innerHTML = text[counter];
  counter++;
  if (counter >= text.length) {
    counter = 0;
    // clearInterval(inst); // uncomment this if you want to stop refreshing after one cycle
  }
}
