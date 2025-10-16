'use strict'

document.addEventListener('DOMContentLoaded', () => {
    let forms = document.querySelectorAll('form.delete-btn')
    forms.forEach(form => {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            event.stopPropagation();

            if (confirm("Are you sure? This cannot be undone!")) {
                event.target.submit();
            }

        })
    })
})