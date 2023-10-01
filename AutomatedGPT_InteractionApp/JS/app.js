function startProcessing() {
    const commandsFile = document.getElementById('commands').files[0];
    const headlinesFile = document.getElementById('headlines').files[0];
    const outputFileName = document.getElementById('outputFileName').value;
    
    if(!commandsFile || !headlinesFile || !outputFileName) {
        alert('Please upload the command and headlines files and enter the output file name.');
        return;
    }
        
    // Hide the app screen and show the processing screen
    document.getElementById('app').style.display = 'none';
    document.getElementById('processingScreen').style.display = 'block';
    
    processFiles(commandsFile, headlinesFile, outputFileName);
}

function processFiles(commandsFile, headlinesFile, outputFileName) {
    // Logic to process the files goes here
    // Update the progress bar and status as the processing progresses
    
    // For illustration:
    let progress = 0;
    let statusElement = document.getElementById('status');
    let progressBar = document.getElementById('progressBar');
    
    // Simulating file processing
    let intervalId = setInterval(() => {
        progress += 10; // Adjust the progress increment as per your logic
        if (progress >= 100) {
            clearInterval(intervalId);
            statusElement.textContent = 'Processing Complete!';
        } else {
            statusElement.textContent = `Processing ${progress}%`;
        }
        progressBar.style.width = progress + '%';
    }, 1000); // Adjust the interval as per your logic

    // At the end of processing
    displayResultScreen(outputFileName);
}

function displayResultScreen(outputFileName) {
    // Hide the processing screen and show the result screen
    document.getElementById('processingScreen').style.display = 'none';
    document.getElementById('resultScreen').style.display = 'block';

    // Update the download link with the generated file.
    let downloadLink = document.getElementById('downloadLink');
    downloadLink.href = outputFileName; // Update the href with the actual path to the generated file.
    downloadLink.download = outputFileName;
}

function resetApp() {
    // Reset the app to its initial state
    document.getElementById('resultScreen').style.display = 'none';
    document.getElementById('app').style.display = 'block';
    
    // Reset the progress bar and status
    document.getElementById('progressBar').style.width = '1%';
    document.getElementById('status').textContent = 'Initializing...';
    
    // Clear the file inputs and output file name input
    document.getElementById('commands').value = '';
    document.getElementById('headlines').value = '';
    document.getElementById('outputFileName').value = '';
}
