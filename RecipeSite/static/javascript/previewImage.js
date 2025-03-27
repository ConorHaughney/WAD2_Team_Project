document.addEventListener('DOMContentLoaded', function () {
    const imageInput = document.getElementById("id_picture");
    const preview = document.getElementById("preview");
    const previewText = document.querySelector(".preview-text");

    if (imageInput) {
        imageInput.addEventListener("change", function (event) {
            const input = event.target;

            if (input.files && input.files[0]) {
                const reader = new FileReader();

                reader.onload = function (e) {
                    preview.src = e.target.result;
                    preview.style.display = "block";
                    previewText.style.display = "none";
                }

                reader.readAsDataURL(input.files[0]);
            } else {
                preview.style.display = "none";
                previewText.style.display = "block";
            }
        });
    }
});