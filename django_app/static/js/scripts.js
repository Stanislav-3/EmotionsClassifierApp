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

    const file_type = e.dataTransfer.files[0].type

    if (e.dataTransfer.files.length && (file_type === 'image/png' || file_type === 'image/jpeg')) {
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
 * @param {Boolean} state
 * @param {Boolean} clickedElement
 */
function updateThumbnail(dropZoneElement, file,
                         state= false, clickedElement = null) {
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

  // Update state
  console.log('update state from callback for .drop-zone__input')
  setIsProcessedState(state)
  activateImage(clickedElement)
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

  console.log('imageClicked')
  activateImage(clickedElement)
  deactivateImages(otherElements)
  uploadActivateImage(clickedElement)
}

function setIsProcessedState(state) {
  console.log('setIsProcessedState', state)
  const isProcessedElement = document.getElementById("is_preprocessed")

  const state_str = state.toString()
  isProcessedElement.value = state_str.charAt(0).toUpperCase() + state_str.slice(1)

  // deactivate image gallery if exists
  if (state === false) {
    const imageGalleryElement = document.getElementById("image-gallery-id")
    if (imageGalleryElement !== null) {
      deactivateImages(Array.from(imageGalleryElement.children))
    }
  }
}


function activateImage(element) {
  if (element === null) return

  element.style.opacity = "1"
}


function deactivateImages(elements) {
  if (elements === null) return

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
  updateThumbnail(dropZoneElement, dataTransfer.files[0], true, element);
}