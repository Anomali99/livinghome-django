var dateBetween = document.querySelector(".date-between");
var listProduct = document.querySelector(".list-product");
var items = document.querySelectorAll(".product");
var form = document.getElementById("myForm");

document.getElementById("cbx-chart").addEventListener("change", function () {
  var value = this.value;

  switch (value) {
    case "1":
      dateBetween.style.display = "none";
      listProduct.style.display = "none";
      form.submit();
      break;
    case "2":
      dateBetween.style.display = "none";
      listProduct.style.display = "flex";
      break;
    case "3":
      dateBetween.style.display = "block";
      listProduct.style.display = "none";
      break;
      case "4":
      dateBetween.style.display = "block";
      listProduct.style.display = "flex";
      break;
  }
});

function selected(id) {
  var item = document.getElementById(`product-${id}`);
  var input = document.getElementById("id_product");
  var selectElement = document.getElementById("cbx-chart")
  input.value = id;
  Array.from(items).forEach((element) => {
    element.style.backgroundColor = "#fff";
  });
  item.style.backgroundColor = "#ddd";
  if (selectElement.value != '4'){
    form.submit();
  }
}

var idProduct = document.getElementById("idProduct").textContent.toString();
var menu = document.getElementById("menu").textContent.toString();
var date_1 = document.getElementById("date_1").textContent.toString();
var date_2 = document.getElementById("date_2").textContent.toString();
var date1Input = document.getElementById("date1");
var date2Input = document.getElementById("date2");

if (menu) {
  var selectElement = document.getElementById("cbx-chart");
  selectElement.selectedIndex = parseInt(menu) - 1;
  switch (menu) {
    case "1":
      dateBetween.style.display = "none";
      listProduct.style.display = "none";
      break;
    case "2":
      dateBetween.style.display = "none";
      listProduct.style.display = "flex";
      var item = document.getElementById(`product-${idProduct}`);
      item.style.backgroundColor = "#ddd";
      break;
      case "3":
        dateBetween.style.display = "block";
        listProduct.style.display = "none";
        date1Input.value = date_1;
      date2Input.value = date_2;
      break;
      case "4":
        dateBetween.style.display = "block";
        listProduct.style.display = "flex";
        date1Input.value = date_1;
        date2Input.value = date_2;
        var item = document.getElementById(`product-${idProduct}`);
        item.style.backgroundColor = "#ddd";
      break;
  }
}
