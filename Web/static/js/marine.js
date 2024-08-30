// Marine Education JavaScript

document.addEventListener('DOMContentLoaded', function () {
    // Highlight the current page in the navigation
    const currentPage = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });

    // Dynamic image gallery (example feature)
    const imageGallery = document.querySelector('.marine-gallery');
    if (imageGallery) {
        imageGallery.addEventListener('click', function (e) {
            if (e.target.tagName === 'IMG') {
                const selectedImage = e.target.src;
                document.querySelector('.featured-image').src = selectedImage;
            }
        });
    }

    // Load more content dynamically (similar to General Education)
    document.querySelectorAll('.load-more').forEach(button => {
        button.addEventListener('click', function () {
            const contentId = this.dataset.contentId;
            document.getElementById(contentId).classList.remove('hidden');
            this.classList.add('hidden'); // Hide the button after loading content
        });
    });
    document.addEventListener('DOMContentLoaded', function () {
        // Add any JavaScript interactions or enhancements here
        console.log('Marine Education JavaScript loaded.');
    });
    

});
