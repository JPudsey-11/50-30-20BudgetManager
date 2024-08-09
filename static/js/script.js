document.addEventListener('DOMContentLoaded', function() {
    // Initialize Materialize CSS modals
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);

    // Handle category input and deletion
    document.querySelector('#categoryInput').addEventListener('keydown', function(e) {
        if (e.keyCode != 13) {
            return;
        }

        e.preventDefault();

        var categoryName = this.value;
        this.value = '';
        addNewCategory(categoryName);
        updateCategoriesString();
    });

    function addNewCategory(name) {
        const html = `<li class="category">
            <span class="name">${name}</span>
            <span onclick="removeCategory(this)" class="btnRemove bold">X</span>
        </li>`;
        document.querySelector('#categoriesContainer').insertAdjacentHTML('beforeend', html);
    }

    function fetchCategoryArray() {
        var categories = [];

        document.querySelectorAll('.category').forEach(function(e) {
            var name = e.querySelector('.name').innerHTML;
            if (name === '') return;

            categories.push(name);
        });

        return categories;
    }

    function updateCategoriesString() {
        categories = fetchCategoryArray();
        document.querySelector('input[name="categoriesString"]').value = categories.join(',');
    }

    function removeCategory(e) {
        e.parentElement.remove();
        updateCategoriesString();
    }

    // Handle income deletion
    document.querySelectorAll('.delete-income').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const incomeId = this.getAttribute('data-id');

            fetch(`/delete_income/${incomeId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.parentElement.parentElement.remove();
                } else {
                    console.error('Failed to delete income');
                }
            });
        });
    });

    // Handle expense deletion
    document.querySelectorAll('.delete-expense').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const expenseId = this.getAttribute('data-id');

            fetch(`/delete_expense/${expenseId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.parentElement.parentElement.remove();
                } else {
                    console.error('Failed to delete expense');
                }
            });
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});