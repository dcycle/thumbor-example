// Provide a function to map unoptimized-to-optimized image URLs.
//
// This script comes from
// https://github.com/dcycle/thumbor-example/tree/master/website-with-large-image/image-mapping.js.

/**
 * Function to load and process image data
 *
 * @param {string} imageServerDomain - The domain of the image server
 *   For example 'https://images.example.com/' or 'http://localhost:8705/'.
 * @param {string} imageFileUrl - The URL of the JSON file containing the image
 *   mapping. For example '/unversioned-image-mapping.json'.
 * @param {string} imageSize - Image size For example '200x', '500x200', 'x250'.
 */
function loadImages(imageServerDomain, imageFileUrl, imageSize) {
  // Select all <img> elements in the document
  const images = document.querySelectorAll('img');

  // Fetch the JSON file once
  fetch(imageFileUrl)
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

              if (!dataSrc) {
                return;
              }

              // Get optimized image URL from mapping data
              let optimizedSrc = mappingData[dataSrc];

              if (optimizedSrc && optimizedSrc[imageSize]) {
                secureurlpart = optimizedSrc[imageSize]
                // Construct the optimized URL
                const optimizedURL = `${secureurlpart}`;

                // Update img src with optimized URL
                img.src = imageServerDomain + optimizedURL;
              }
              else {
                // using imageFileUrl, we cannot map the unoptimized image to
                // an optimized image. We will use the original image.
                img.src = dataSrc;
              }
          });
      })
      .catch(error => {
          console.error('Error fetching or processing JSON:', error);
          // Optionally handle error, e.g., set a fallback image for all images
      });
}
