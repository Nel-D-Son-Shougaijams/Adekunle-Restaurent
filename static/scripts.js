
    // Select buttons and divs
    const buttons = document.querySelectorAll('.button-group button');
    const divs = document.querySelectorAll('.category-section');

    // Ensure one tab is always open (default to the first tab)
    divs.forEach(div => div.style.display = 'none'); // Hide all divs initially
    if (divs.length > 0) {
        divs[0].style.display = 'block'; // Show the first div
    }

    // Highlight the first button to indicate it is active
    if (buttons.length > 0) {
        buttons[0].classList.add('active');
    }

    // Loop through buttons and add event listeners
    buttons.forEach((button, index) => {
        button.addEventListener('click', () => {
            // Hide all divs
            divs.forEach(div => div.style.display = 'none');
            
            // Show the clicked div
            divs[index].style.display = 'block';

            // Remove 'active' class from all buttons
            buttons.forEach(btn => btn.classList.remove('active'));

            // Add 'active' class to the clicked button
            button.classList.add('active');
        });
    });
    const accordionHeaders = document.querySelectorAll(".accordion-header");

accordionHeaders.forEach(header => {
  header.addEventListener("click", () => {
    const accordionContent = header.nextElementSibling;

    // Toggle the current accordion
    accordionContent.classList.toggle("open");

    // Close other accordions
    document.querySelectorAll(".accordion-content").forEach(content => {
      if (content !== accordionContent) {
        content.classList.remove("open");
      }
    });
  });
});