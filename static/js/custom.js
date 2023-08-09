// Get a reference to the error alert element
var errorAlert = document.getElementById('errorAlert');
		
// Function to hide the alert after a delay
function hideAlert() {
    errorAlert.style.display = 'none';
}

// Set a delay (in milliseconds) before hiding the alert
var delay = 5000; // 5 seconds
setTimeout(hideAlert, delay);