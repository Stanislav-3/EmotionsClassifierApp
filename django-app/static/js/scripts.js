document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
  const dropZoneElement = inputElement.closest(".drop-zone");

  dropZoneElement.addEventListener("click", (e) => {
    console.log('2')
    inputElement.click();
  });

  inputElement.addEventListener("change", (e) => {
    console.log('3')
    if (inputElement.files.length) {
      updateThumbnail(dropZoneElement, inputElement.files[0]);
    }
  });

  dropZoneElement.addEventListener("dragover", (e) => {
    console.log('4')
    e.preventDefault();
    dropZoneElement.classList.add("drop-zone--over");
  });

  ["dragleave", "dragend"].forEach((type) => {
    dropZoneElement.addEventListener(type, (e) => {
      console.log('5')
      dropZoneElement.classList.remove("drop-zone--over");
    });
  });

  dropZoneElement.addEventListener("drop", (e) => {
    console.log('6')
    e.preventDefault();

    if (e.dataTransfer.files.length) {
      inputElement.files = e.dataTransfer.files;
      updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
    }

    dropZoneElement.classList.remove("drop-zone--over");
  });
});

/**
 * Updates the thumbnail on a drop zone element.
 *
 * @param {HTMLElement} dropZoneElement
 * @param {File} file
 */
function updateThumbnail(dropZoneElement, file) {
  console.log('1')
  let thumbnailElement= dropZoneElement.querySelector(".drop-zone__thumb");

  // First time - remove the prompt
  if (dropZoneElement.querySelector(".drop-zone__prompt")) {
    dropZoneElement.querySelector(".drop-zone__prompt").remove();
  }

  // First time - there is no thumbnail element, so lets create it
  if (!thumbnailElement) {
    thumbnailElement = document.createElement("div");
    thumbnailElement.classList.add("drop-zone__thumb");
    dropZoneElement.appendChild(thumbnailElement);
  }

  thumbnailElement.dataset.label = file.name;

  // Show thumbnail for image files
  if (file.type.startsWith("image/")) {
    console.log('-2')
    const reader = new FileReader();

    reader.readAsDataURL(file);
    reader.onload = () => {
      thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
    };
  } else {
    console.log('-1')
    thumbnailElement.style.backgroundImage = null;
  }
}



// Image gallery thing
function imageClicked(image_id, images_count) {
  const id_prefix = "gallery_image_"

  const clickedElement = document.getElementById(image_id)

  let otherElements = []
  for(let i = 0; i < images_count; i += 1) {
    otherElements.push(
        document.getElementById(id_prefix + i)
    )
  }

  otherElements = otherElements.filter((value) => {
    return value.id !== clickedElement.id
  })

  activateImage(clickedElement)
  deactivateImages(otherElements)
  uploadActivateImage(clickedElement)
}


function activateImage(element) {
  element.style.opacity = "1"
}


function deactivateImages(elements) {
  elements.forEach((element) => element.style.opacity = "0.2")
}


 function dataURLtoFile(dataurl, filename) {
        let arr = dataurl.split(','),
            mime = arr[0].match(/:(.*?);/)[1],
            bstr = atob(arr[1]),
            n = bstr.length,
            u8arr = new Uint8Array(n);

        while(n--){
            u8arr[n] = bstr.charCodeAt(n);
        }

        return new File([u8arr], filename, {type:mime});
    }


function uploadActivateImage(element) {
  const base64Image = element.getElementsByTagName("img")[0].src
  let imageName = 'some_name.jpeg'

  const dropZoneElement = document.getElementById("drop_zone_id");

  // Make a file
  const fileElement = document.getElementsByClassName("drop-zone__input")[0];
  const dataTransfer = new DataTransfer();

  dataTransfer.items.add(dataURLtoFile(base64Image, imageName));
  fileElement.files = dataTransfer.files;

  // Update
  updateThumbnail(dropZoneElement, dataTransfer.files[0]);
}