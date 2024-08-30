// General Education JavaScript

document.addEventListener('DOMContentLoaded', function () {
    // Highlight the current page in the navigation
    const currentPage = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });

    // Example of dynamic content loading (if needed in future)
    document.querySelectorAll('.load-more').forEach(button => {
        button.addEventListener('click', function () {
            const contentId = this.dataset.contentId;
            document.getElementById(contentId).classList.remove('hidden');
            this.classList.add('hidden'); // Hide the button after loading content
        });
    });
    document.addEventListener('DOMContentLoaded', function () {
        // Add any JavaScript interactions or enhancements here
        console.log('General Education JavaScript loaded.');
    });
    
});
