document.getElementById("sendUrl").addEventListener("click", function() {
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    let activeTab = tabs[0];
    let url = activeTab.url;

    if (url.includes("linkedin.com")) {
      fetch("http://192.168.0.16:5000/api/url", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error("Ошибка ответа сервера");
        }
        // Извлекаем имя файла из заголовка Content-Disposition
        const contentDisposition = response.headers.get('Content-Disposition');

        const fileName = contentDisposition
            ? contentDisposition.split('filename=')[1].replace(/"/g, '')
            : 'downloaded_file.docx';

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
      });
    } else {
      document.getElementById("status").textContent = "Это не страница LinkedIn";
    }
  });
});
