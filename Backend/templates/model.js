// Select the model-viewer element from the HTML
const modelViewer = document.getElementById('modelViewer');

// Fetch the PID from the backend and load the appropriate model
async function fetchAndLoadModel() {
  try {
    // Fetch the PID and model data from the backend
    const response = await fetch('http://127.0.0.1:5000/api/get3D/${PID}'); //

    if (!response.ok) {
      throw new Error(`Server error: ${response.statusText}`);
    }

    // Parse the response to get model data
    const data = await response.json();
    const modelUrl = data.url;  // Model URL 
    const PID = data.PID;  // PID 

    console.log(`Model URL: ${modelUrl}, PID: ${PID}`); // For debugging

    // Detect the OS and use correct model
    const platform = detectOS();
    if (platform === 'ios') {
      modelViewer.setAttribute('ios-src', modelUrl);  // iOS model (usdz)
    } else {
      modelViewer.setAttribute('src', modelUrl);  // Android/Web model (glb)
    }
  } catch (error) {
    console.error('Error fetching or loading the model:', error);
  }
}

// Call the function to fetch and load the model when the page loads
await fetchAndLoadModel();
