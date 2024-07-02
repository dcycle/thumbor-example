// script.js

// Function to load and process image data
function loadImages() {
  // Select all <img> elements in the document
  const images = document.querySelectorAll('img');

  // Fetch the JSON file once
  fetch('unversioned-image-mapping.json')
      .then(response => {
          if (!response.ok) {
              throw new Error('Failed to fetch JSON');
          }
          return response.json();
      })
      .then(mappingData => {
          // Iterate over each <img> element
          images.forEach(img => {
              // Read data attributes
              const dataSrc = img.getAttribute('data-src');
              const dataSize = img.getAttribute('data-size');
              const dataServer = img.getAttribute('data-server');

              // Get optimized image URL from mapping data
              const optimizedSrc = mappingData[dataSrc];

              if (!optimizedSrc) {
                  console.error(`Optimized image not found for src: ${dataSrc}`);
                  return; // Skip this image if optimized src is not found
              }

              // Construct the optimized URL
              const optimizedURL = `${optimizedSrc}`;

              // Update img src with optimized URL
              img.src = optimizedURL;
          });
      })
      .catch(error => {
          console.error('Error fetching or processing JSON:', error);
          // Optionally handle error, e.g., set a fallback image for all images
      });
}

// Event listener to execute loadImages function when the page is fully loaded
window.addEventListener('load', loadImages);
