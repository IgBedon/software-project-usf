// JavaScript para exibir o nome do arquivo selecionado
document.addEventListener("DOMContentLoaded", function() {
    const fileInput = document.getElementById('task_attachment');
    const fileLabel = document.getElementById('file-label');
  
    if (fileInput) {
      fileInput.addEventListener('change', function () {
        if (fileInput.files.length > 0) {
          fileLabel.textContent = fileInput.files[0].name;
        } else {
          fileLabel.textContent = 'Adicionar arquivo';
        }
      });
    }
  });
  