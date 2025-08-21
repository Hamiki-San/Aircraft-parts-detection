const dropZone = document.getElementById('drop-zone');
const fileInput = document.querySelector('.drop-zone__input');
const processedImage = document.getElementById('processed-image');
const detectionData = document.getElementById('detection-data');

dropZone.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    if (fileInput.files.length) {
        handleFile(fileInput.files[0]);
    }
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length) {
        handleFile(files[0]);
    }
});

function handleFile(file) {
    const formData = new FormData();
    formData.append('image', file);

    // Reset previous results
    processedImage.style.display = 'none';
    detectionData.textContent = 'Processing...';

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.status === 'success') {
            // Display the processed image
            processedImage.src = data.processed_image_url;
            processedImage.style.display = 'block';

            // Display the detection data as a formatted string
            detectionData.textContent = JSON.stringify(data, null, 2);
        } else {
            detectionData.textContent = 'Error: ' + data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        detectionData.textContent = 'An error occurred during file upload.';
    });
}