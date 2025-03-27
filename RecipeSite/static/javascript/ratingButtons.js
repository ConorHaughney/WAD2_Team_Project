document.addEventListener('DOMContentLoaded', function () {
    const ratingButtons = document.querySelectorAll('.rating-btn');
    const ratingInput = document.getElementById('id_rating');

    for (let i = 0; i < ratingButtons.length; i++) {
        ratingButtons[i].addEventListener('click', function () {
            const selectedValue = parseInt(this.dataset.value);

            for (let j = 0; j < ratingButtons.length; j++) {
                ratingButtons[j].classList.remove('active');
            }
            
            this.classList.add('active');

            ratingInput.value = selectedValue;
        });
    }
});