// scripts.js

document.addEventListener('DOMContentLoaded', () => {
    console.log('RRSMEDIA Github Repository Loaded');

    // Example: Add a click event to navigation links
    const navLinks = document.querySelectorAll('nav ul li a');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            alert(`You clicked on ${link.textContent}`);
        });
    });
});
