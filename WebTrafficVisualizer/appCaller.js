function loadTrafficData(startTime, endTime) {
    const encodedStartTime = encodeURIComponent(startTime);
    const encodedEndTime = encodeURIComponent(endTime);

    const apiUrl = `http://localhost:5000/trafficdata?start_time=${encodedStartTime}&end_time=${encodedEndTime}`;

    return fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                return Promise.reject(new Error(`Network response was not ok (${response.status})`));
            }
            return response.json();
        });
}