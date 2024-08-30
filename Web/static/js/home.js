document.addEventListener('DOMContentLoaded', function () {
    // Initialize Smooth Scroll for anchor links
    const scroll = new SmoothScroll('a[href*="#"]', {
        speed: 600,
        speedAsDuration: true
    });

    // Initialize Bootstrap carousel if needed
    const carouselElement = document.querySelector('#newsCarousel');
    if (carouselElement) {
        const carousel = new bootstrap.Carousel(carouselElement, {
            interval: 5000, // Change slide every 5 seconds
            wrap: true // Cycle through items
        });
    }
});
