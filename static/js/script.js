document.addEventListener('DOMContentLoaded', function() {
    // Initialize Materialize CSS modals
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);

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
                    document.getElementById(`income-${incomeId}`).remove();
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
                    document.getElementById(`expense-${expenseId}`).remove();
                } else {
                    console.error('Failed to delete expense');
                }
            });
        });
    });

    // Function to set the category when opening the modal
    window.setCategory = function(category) {
        document.getElementById('categoryInput').value = category;
    };

    // Helper function to get CSRF token
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
