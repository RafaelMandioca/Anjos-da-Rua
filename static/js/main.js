// static/js/main.js

console.log("Hello from main.js!");

document.addEventListener('DOMContentLoaded', (event) => {
    const heading = document.querySelector('h1');
    heading.addEventListener('click', () => {
        alert('You clicked the heading!');
    });
});