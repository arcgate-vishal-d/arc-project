function startTestTimer() {
    var startTime = null;
    var timerInterval = null;

    // Listen for keyup events on the document
    document.addEventListener("keyup", function (event) {
        // If the timer hasn't started yet, set the start time and start the timer
        if (startTime === null) {
            startTime = new Date().getTime();
            timerInterval = setInterval(updateTimer, 1000);
        }
    });

    // Update the timer display every second
    function updateTimer() {
        var elapsedTime = new Date().getTime() - startTime;
        var seconds = Math.floor(elapsedTime / 1000);
        var minutes = Math.floor(seconds / 60);
        seconds = seconds % 60;
    }
}
