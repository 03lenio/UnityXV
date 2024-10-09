window.addEventListener('load', function () {
    document.getElementById("submitBtn").addEventListener("click", function() {
                const userInput = document.getElementById("promptInput").value;

                // Send the input data to the server via AJAX
                fetch("/query", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ prompt: userInput })
                })
                .then(response => response.json())
                .then(data => {
                    // Update the textarea with the response from the server
                    document.getElementById("outputTextArea").value = data.result;
                })
                .catch(error => console.error('Error:', error));
            });
  })