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

document.addEventListener("DOMContentLoaded", () => {
  // Toggle "Other" input for study_place
  const studyPlaceOtherCheckbox = document.querySelector("input[name='study_place'][value='other']");
  const studyPlaceOtherInputContainer = document.getElementById("study_place_other_container");

  if (studyPlaceOtherCheckbox && studyPlaceOtherInputContainer) {
    function toggleStudyPlaceOther() {
      studyPlaceOtherInputContainer.style.display = studyPlaceOtherCheckbox.checked ? "block" : "none";
    }
    studyPlaceOtherCheckbox.addEventListener("change", toggleStudyPlaceOther);
    toggleStudyPlaceOther(); // initialize on page load
  }

  // Similarly, add toggles for other "Other" inputs if needed, e.g.:
  // live_with_other, highest_education_other, marital_status_other, house_type_other, transport_mode_other, personality_traits_other
  // Example for live_with_other:
  const liveWithOtherCheckbox = document.querySelector("input[name='live_with'][value='other']");
  const liveWithOtherInputContainer = document.getElementById("live_with_other_container");
  if (liveWithOtherCheckbox && liveWithOtherInputContainer) {
    function toggleLiveWithOther() {
      liveWithOtherInputContainer.style.display = liveWithOtherCheckbox.checked ? "block" : "none";
    }
    liveWithOtherCheckbox.addEventListener("change", toggleLiveWithOther);
    toggleLiveWithOther();
  }
});
