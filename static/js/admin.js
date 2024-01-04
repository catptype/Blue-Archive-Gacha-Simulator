function previewImage(input, previewEL, original) {
    var preview = document.getElementById(previewEL);
    var fileInput = document.getElementById('id_image');
    var file = input.files[0];
    var reader = new FileReader();

    reader.onloadend = function () {
        preview.src = reader.result;
    };

    if (file && file.type.startsWith('image/')) {
        reader.readAsDataURL(file);
    } else if (file && !file.type.startsWith('data/')) {
        alert('Please select a valid image file.');
        fileInput.value = '';
        preview.src = original || "/static/portrait_404.png";
    } else {
        preview.src = original || "/static/portrait_404.png";
    }
}

function clearImage(previewEL, original) {
    var preview = document.getElementById(previewEL);
    var fileInput = document.getElementById('id_image');
    
    fileInput.value = '';
    preview.src = original || "/static/portrait_404.png";
}