var imageLists = document.querySelectorAll(".image-list");

function setImagePreview(url, filename) {
  var imagePreview = document.getElementById("preview-image");
  var imageList = document.getElementById(`list-${filename}`);

  Array.from(imageLists).forEach((element) => {
    element.style.border = "2px solid #aaa";
  });
  imagePreview.src = url + filename;
  imageList.style.border = "2px solid #000";
}

imageLists[0].style.border = "2px solid #000";

function cancelComment() {
  var comment = document.getElementById("comment");
  comment.style.display = "none";
}

function addComment() {
  var comment = document.getElementById("comment");
  comment.style.display = "flex";
}
