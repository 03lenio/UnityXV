window.addEventListener('load', function () {
    document.getElementById("outputTextArea").addEventListener("change", function () {
        const text = document.getElementById("outputTextArea").value;
        fetch(`/synthesize/${encodeURIComponent(text)}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        }).then(response => {
        if (!response.ok) {
            throw new Error("Failed to fetch audio.");
        }
        return response.blob(); // Get the audio data as a Blob
        })
        .then(audioBlob => {
            // Create a URL for the Blob and play it
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            audio.play();
        })
        .catch(error => {
            console.error("Error playing audio:", error);
        });
    })

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
                    const outputTextArea = document.getElementById("outputTextArea");
                    outputTextArea.value = data.result;

                    // Manually trigger the change event
                    const event = new Event('change', { bubbles: true });
                    outputTextArea.dispatchEvent(event);
                    document.getElementById("promptInput").value = "";
                })
                .catch(error => console.error('Error:', error));
            });
  })