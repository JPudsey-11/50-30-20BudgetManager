document.addEventListener('DOMContentLoaded', function() {
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

    // Financial function to format numbers to two decimal places
    function financial(x) {
        return Number.parseFloat(x).toFixed(2);
    }

    // Initialize Materialize CSS modals
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);

    // Apply financial formatting to percentages
    const fundamentalsPercentageElement = document.getElementById('fundamentals-percentage');
    const funPercentageElement = document.getElementById('fun-percentage');
    const futureYouPercentageElement = document.getElementById('future-you-percentage');

    if (fundamentalsPercentageElement && funPercentageElement && futureYouPercentageElement) {
        fundamentalsPercentageElement.textContent = financial(fundamentalsPercentageElement.textContent) + '%';
        funPercentageElement.textContent = financial(funPercentageElement.textContent) + '%';
        futureYouPercentageElement.textContent = financial(futureYouPercentageElement.textContent) + '%';
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

            fetch(`/get_income/${incomeId}/`, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('income-id').value = data.income.id;
                    document.getElementById('id_source').value = data.income.source;
                    document.getElementById('id_planned_amount').value = data.income.planned_amount;
                    document.getElementById('id_received_amount').value = data.income.received_amount;
                    M.Modal.getInstance(document.getElementById('addIncomeModal')).open();
                } else {
                    console.error('Failed to fetch income data');
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

    // Handle expense edit
    document.querySelectorAll('.edit-expense').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const expenseId = this.getAttribute('data-id');

            fetch(`/get_expense/${expenseId}/`, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('expense-id').value = data.expense.id;
                    document.getElementById('id_description').value = data.expense.description;
                    document.getElementById('id_planned_amount').value = data.expense.planned_amount;
                    document.getElementById('id_spent_amount').value = data.expense.spent_amount;
                    document.getElementById('categoryInput').value = data.expense.category;
                    M.Modal.getInstance(document.getElementById('addExpenseModal')).open();
                } else {
                    console.error('Failed to fetch expense data');
                }
            });
        });
    });

    // Function to set the category when opening the modal
    window.setCategory = function(category) {
        document.getElementById('categoryInput').value = category;
    };
});