// Check if section is selected on page load
document.addEventListener('DOMContentLoaded', function() {
    checkActiveSection();
});

function checkActiveSection() {
    fetch('/teacher/api/get-active-section/')
        .then(response => response.json())
        .then(data => {
            if (data.has_section) {
                // Auto-select section in dropdowns
                const sectionSelects = document.querySelectorAll('select[name="section"], #section-select');
                sectionSelects.forEach(select => {
                    if (select) {
                        select.value = data.section.id;
                        // Trigger change event to load data
                        select.dispatchEvent(new Event('change'));
                    }
                });
            }
        });
}