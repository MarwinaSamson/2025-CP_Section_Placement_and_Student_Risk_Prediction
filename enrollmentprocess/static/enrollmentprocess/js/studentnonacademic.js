document.addEventListener("DOMContentLoaded", function() {
    // For checkboxes where only one option is allowed
    document.querySelectorAll('.checkbox-options[data-single="true"]').forEach(group => {
        let checkboxes = group.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(cb => {
            cb.addEventListener('change', function() {
                if (this.checked) {
                    checkboxes.forEach(other => {
                        if (other !== this) other.checked = false;
                    });
                }
            });
        });
    });
});