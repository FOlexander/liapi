document.getElementById("sendUrl").addEventListener("click", function() {
  const loader = document.getElementById("loader");
  const statusText = document.getElementById("status");
  
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    let activeTab = tabs[0];
    let url = activeTab.url;

    if (url.includes("linkedin.com/in/")) {
      loader.classList.remove("hidden");

      fetch("http://127.0.0.1:5000/api/url", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: url })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error("Server error, please try again later");
        }
        // Извлекаем имя файла из заголовка Content-Disposition
        const contentDisposition = response.headers.get('Content-Disposition');

        const fileName = contentDisposition
            ? contentDisposition.split('filename=')[1].replace(/"/g, '')
            : 'downloaded_file.docx';

        document.getElementById("status").textContent = "Profile captured!";
        document.getElementById("download-link").classList.remove("hidden");

        return response.blob().then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = fileName;
            document.body.appendChild(a);
            a.click();

            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        });
      })
      .catch(error => {
        console.error("Failed to send URL:", error);
        document.getElementById("status").textContent = error.message;
      })
      .finally(() => {
        loader.classList.add("hidden");
      });
    } else {
      document.getElementById("status").textContent = "Not a LinkedIn page profile page";
    }
  });
});
