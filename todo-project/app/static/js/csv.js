import { generateFileName } from "./config.js";

document.addEventListener("DOMContentLoaded", () => {
  const controls = document.querySelector(".controls");
  const exportUrl = controls.dataset.exportUrl;
  const importUrl = controls.dataset.importUrl;

  const exportBtn = document.getElementById("export-btn");
  const importBtn = document.getElementById("import-btn");
  const importFile = document.getElementById("import-file");

  exportBtn.addEventListener("click", () => {
    const originalButtonText = exportBtn.textContent;
    exportBtn.disabled = true;
    exportBtn.textContent = "エクスポート処理中...";

    fetch(exportUrl)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network Response was not ok" + response.statusText);
        }
        return response.blob();
      })
      .then((blob) => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.style.display = "none";
        a.href = url;

        a.download = generateFileName();
        document.body.appendChild(a);
        a.click();

        // メモリリークを防ぐためにURLを開放する。
        URL.revokeObjectURL(url);

        alert("CSVファイルのエクスポートが完了しました。");
      })
      .catch((error) => {
        console.error(
          "There has been a problem with your fetch operation:",
          error
        );
        alert("CSVファイルのエクスポートに失敗しました。");
      })
      .finally(() => {
        exportBtn.disabled = false;
        exportBtn.textContent = originalButtonText;
      });
  });

  importBtn.addEventListener("click", () => {
    importFile.click();
  });

  importFile.addEventListener("change", (event) => {
    const file = event.target.files[0];

    if (file) {
      const formData = new FormData();
      formData.append("file", file);

      fetch(importUrl, {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          alert(data.message);
          if (data.success) {
            const taskId = data.task_id;
            const interval = setInterval(() => {
              fetch(`/todos/import_status/${taskId}`)
                .then((res) => res.json())
                .then((statusData) => {
                  if (statusData.status === "done") {
                    clearInterval(interval);
                    alert("インポート完了！");
                    location.reload();
                  } else if (statusData.status === "error") {
                    clearInterval(interval);
                    alert("インポート失敗: " + statusData.message);
                  }
                });
            }, 2000);
          } else {
            alert(data.message);
          }
        })
        .catch((error) => {
          console.error("Error", error);
          alert("CSVインポートに失敗しました。");
        });
    }

    // changeイベントを前回と同じファイルを選択しても発火させたいため。
    event.target.value = null;
  });
});
