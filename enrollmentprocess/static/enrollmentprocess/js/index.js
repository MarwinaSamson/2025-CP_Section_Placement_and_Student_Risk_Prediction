document.addEventListener("DOMContentLoaded", () => {
  const images = document.querySelectorAll(".carousel-image")
  const dots = document.querySelectorAll(".dot")
  const prevButton = document.querySelector(".prev-button")
  const nextButton = document.querySelector(".next-button")
  let currentIndex = 0

      function updateCarousel() {
        // Hide all images and deactivate all dots
        images.forEach((image) => image.classList.remove("active"))
        dots.forEach((dot) => dot.classList.remove("active"))

        // Show the current image and activate the current dot
        images[currentIndex].classList.add('active');
        dots[currentIndex].classList.add('active');
    }

    // Event listener for the "next" button
    nextButton.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % images.length;
        updateCarousel();
    });

    // Event listener for the "previous" button
    prevButton.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        updateCarousel();
    });

    // Event listeners for the navigation dots
    dots.forEach((dot) => {
        dot.addEventListener("click", () => {
        const dotIndex = Number.parseInt(dot.getAttribute("data-index"))
        currentIndex = dotIndex
        updateCarousel()
        })
    })

    // Initial call to set up the carousel on page load
    updateCarousel()
})