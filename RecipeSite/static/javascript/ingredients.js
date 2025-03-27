document.addEventListener('DOMContentLoaded', function () {
    const addIngredientBtn = document.getElementById('add-ingredient');
    const ingredientsContainer = document.getElementById('ingredients-container');

    addIngredientBtn.addEventListener('click', function () {
        const ingredientRow = document.createElement('div');
        ingredientRow.className = 'ingredient-row form-row';

        const nameGroup = document.createElement('div');
        nameGroup.className = 'form-group half';
        const nameLabel = document.createElement('label');
        nameLabel.textContent = 'Ingredient Name:';
        const nameInput = document.createElement('input');
        nameInput.type = 'text';
        nameInput.name = 'ingredient_names[]';
        nameInput.maxLength = 15;
        nameInput.required = true;

        const quantityGroup = document.createElement('div');
        quantityGroup.className = 'form-group half';
        const quantityLabel = document.createElement('label');
        quantityLabel.textContent = 'Quantity:';
        const quantityInput = document.createElement('input');
        quantityInput.type = 'number';
        quantityInput.name = 'ingredient_quantities[]';
        quantityInput.min = 1;
        quantityInput.max = 10000;
        quantityInput.required = true;

        const removeButton = document.createElement('button');
        removeButton.type = 'button';
        removeButton.className = 'remove-ingredient';
        removeButton.textContent = 'X';
        removeButton.onclick = function () {
            this.parentElement.remove();
        };

        nameGroup.appendChild(nameLabel);
        nameGroup.appendChild(nameInput);
        quantityGroup.appendChild(quantityLabel);
        quantityGroup.appendChild(quantityInput);
        ingredientRow.appendChild(nameGroup);
        ingredientRow.appendChild(quantityGroup);
        ingredientRow.appendChild(removeButton);

        ingredientsContainer.appendChild(ingredientRow);
    });
});