// Toggle menu function for navigation
function toggleMenu() {
    var navLinks = document.getElementById("navLinks");
    navLinks.classList.toggle("active");
}

// General DOMContentLoaded listener to handle page-specific scripts
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on page 2
    if (document.getElementById('model-select-form')) {
        setupModelSelectPage();
    }

    // Check if we're on page 3 (camera.html)
    if (document.getElementById('uploadFile')) {
        setupCameraPage();
    }

    // Check if we're on page 4 (project.html)
    if (document.getElementById('postName')) {
        setupProjectPage();
    }
});

// Function to handle page 2 (Model Select Page)
function setupModelSelectPage() {
    let treeCount = document.getElementById('treeCount');
    let flowerCount = document.getElementById('flowerCount');
    let bushCount = document.getElementById('bushCount');

    setupCounter(treeCount, 'plusTree', 'minusTree');
    setupCounter(flowerCount, 'plusFlower', 'minusFlower');
    setupCounter(bushCount, 'plusBush', 'minusBush');

    // Submit Form and Redirect to Camera Page (Page 3)
    document.getElementById('model-select-form').addEventListener('submit', function (event) {
        event.preventDefault();
        window.location.href = 'camera.html';
    });
}

// Generic counter setup function for trees, flowers, and bushes
function setupCounter(element, plusId, minusId) {
    document.getElementById(plusId).addEventListener('click', function () {
        if (parseInt(element.value) < 10) {
            element.value = parseInt(element.value) + 1;
        }
    });

    document.getElementById(minusId).addEventListener('click', function () {
        if (parseInt(element.value) > 0) {
            element.value = parseInt(element.value) - 1;
        }
    });
}

// Function to handle page 3 (Camera Page)
function setupCameraPage() {
    // Post Button redirect to Project Page (Page 4)
    document.getElementById('postBtn').addEventListener('click', function () {
        window.location.href = 'project.html';
    });

    // File upload validation for PNG files
    document.getElementById('uploadFile').addEventListener('change', function () {
        const file = this.files[0];
        if (file && file.type === 'image/png') {
            console.log('PNG file selected:', file.name);
        } else {
            alert('Please select a valid PNG image.');
            this.value = ''; // Clear the input if invalid
        }
    });
}

// Function to handle page 4 (Project Page)
function setupProjectPage() {
    // Example data (replace with actual API or dynamic data)
    const postData = {
        postName: "Tree Planting - Central Park",
        description: "Urban greening initiative in NYC's Central Park.",
        uploadedImage: "path-to-your-image.png", // Add a valid image path here
        location: "New York City, USA"
    };

    // Populate the post data into the HTML
    document.getElementById('postName').textContent = postData.postName;
    document.getElementById('description').textContent = postData.description;
    document.getElementById('uploadedImage').src = postData.uploadedImage;
    document.getElementById('uploadedImage').alt = postData.postName;
    document.querySelector('p strong').nextSibling.textContent = ` ${postData.location}`;

    // Donate button action
    document.getElementById('donateBtn').addEventListener('click', function () {
        window.location.href = 'payment.html';
    });

    
}


//Geolocation 
/* It the location popup doesn't work with the mobile browsers currently

document.addEventListener('DOMContentLoaded', function () {
    let geolocationActive = false;

    // Check if geolocation was already activated in the current session
    const geolocationActivated = localStorage.getItem('geolocationActivated');

    // If geolocation is not yet activated, proceed with blocking and requesting location
    if (!geolocationActivated) {
        blockWebsiteUntilGeolocation();
    } else {
        allowAccessToWebsite(); // If geolocation was activated previously, allow access immediately
    }

    // Function to block the website and request geolocation continuously
    function blockWebsiteUntilGeolocation() {
        // Hide or disable all website content interaction
        document.body.style.pointerEvents = "none";
        document.body.style.opacity = "0.5";

        alert("Please activate location services to access the website.");

        // Continuously check for geolocation every 3 seconds
        const locationInterval = setInterval(() => {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function (position) {
                    showPosition(position);
                    geolocationActive = true;
                    allowAccessToWebsite(); // Allow access once location is obtained
                    clearInterval(locationInterval); // Stop checking once location is enabled 

                    // Store the state in localStorage to prevent future prompts
                    localStorage.setItem('geolocationActivated', 'true');
                }, showError);
            } else {
                document.getElementById('location-info').innerHTML = '<p class="text-danger">Geolocation is not supported by your browser.</p>';
                clearInterval(locationInterval); // Stop checking if geolocation is unsupported
            }
        }, 3000); // Check every 3 seconds
    }

    // Function to allow access to the website once geolocation is active
    function allowAccessToWebsite() {
        document.body.style.pointerEvents = "auto"; // Re-enable interaction
        document.body.style.opacity = "1"; // Restore normal visibility
    }

    // Function to display location and accuracy
    function showPosition(position) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        const accuracy = position.coords.accuracy; // Get accuracy value in meters
        console.log(`Latitude: ${lat}, Longitude: ${lon}, Accuracy: ${accuracy} meters`);
    }

    // Function to handle geolocation errors
    function showError(error) {
        let message;
        switch (error.code) {
            case error.PERMISSION_DENIED:
                message = "User denied the request for Geolocation.";
                break;
            case error.POSITION_UNAVAILABLE:
                message = "Location information is unavailable.";
                break;
            case error.TIMEOUT:
                message = "The request to get user location timed out.";
                break;
            case error.UNKNOWN_ERROR:
                message = "An unknown error occurred.";
                break;
        }
        document.getElementById('location-info').innerHTML = `<p class="text-danger">${message}</p>`;
    }
});
*/