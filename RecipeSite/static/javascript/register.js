document.addEventListener("DOMContentLoaded", function() {
    // prevents the user from being able to scroll the page
    document.body.style.overflow = "hidden";
    document.documentElement.style.overflow = "hidden";

    // displays a preview of the uploaded profile picture
    document.getElementById("id_picture").addEventListener("change", function(event) {
        var input = event.target;
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                var preview = document.getElementById("preview");
                preview.src = e.target.result;
                preview.style.display = "block";
            }
            reader.readAsDataURL(input.files[0]);
        }
    });

    // checks if the password input matches the confirm password input
    const passwordInput = document.getElementById("id_password");
    const confirmPasswordInput = document.getElementById("id_confirm_password");
    const messageSpan = document.getElementById("password-match-message");

    function validatePasswordMatch() {
        // if passwords dont match display message to the user
        if (passwordInput.value && confirmPasswordInput.value && passwordInput.value !== confirmPasswordInput.value) {
            messageSpan.textContent = "Passwords do not match";
        } else {
            messageSpan.textContent = "";
        }
    }

    passwordInput.addEventListener("input", validatePasswordMatch);
    confirmPasswordInput.addEventListener("input", validatePasswordMatch);
});