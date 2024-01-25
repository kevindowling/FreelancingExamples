$(document).ready(function() {
    // Set the beginning and end times
    var beginning = new Date("2023-10-20T00:00:00Z").getTime(); // 10/20/2023 00:00 UTC
    var end = Date.now(); // current time in UTC
  
    // Function to format the selected time range
    function formatDateRange(values) {
      var startTime = new Date(values[0]);
      var endTime = new Date(values[1]);
  
      return startTime.toUTCString() + ' - ' + endTime.toUTCString();
    }
  
    // Create the slider
    $("#slider-range").slider({
      range: true,
      min: beginning,
      max: end,
      step: 60000, // steps of 1 minute
      values: [beginning, end], // initial range settings
      slide: function(event, ui) {
        // When the slider values change, update the displayed time range
        $("#timeRange").text(formatDateRange(ui.values));
      }
    });
  
    // Set the initial time range text
    $("#timeRange").text(formatDateRange($("#slider-range").slider("values")));
  });