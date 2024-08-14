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

    // Handle income edit
    document.querySelectorAll('.edit-income').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const incomeId = this.getAttribute('data-id');
            const source = this.getAttribute('data-source');
            const plannedAmount = this.getAttribute('data-planned-amount');
            const receivedAmount = this.getAttribute('data-received-amount');

            document.getElementById('income-id').value = incomeId;
            document.getElementById('income-source').value = source;
            document.getElementById('income-planned-amount').value = plannedAmount;
            document.getElementById('income-received-amount').value = receivedAmount;

            M.Modal.getInstance(document.getElementById('addIncomeModal')).open();
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

    // Handle expense edit
    document.querySelectorAll('.edit-expense').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const expenseId = this.getAttribute('data-id');
            const description = this.getAttribute('data-description');
            const plannedAmount = this.getAttribute('data-planned-amount');
            const spentAmount = this.getAttribute('data-spent-amount');
            const category = this.getAttribute('data-category');

            document.getElementById('expense-id').value = expenseId;
            document.getElementById('expense-description').value = description;
            document.getElementById('expense-planned-amount').value = plannedAmount;
            document.getElementById('expense-spent-amount').value = spentAmount;
            document.getElementById('categoryInput').value = category;

            M.Modal.getInstance(document.getElementById('addExpenseModal')).open();
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
