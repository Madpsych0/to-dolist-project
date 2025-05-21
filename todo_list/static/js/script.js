document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("taskForm");
  const input = document.getElementById("taskInput");

  // Prevent empty submissions (double check)
  form.addEventListener("submit", (e) => {
    if (!input.value.trim()) {
      e.preventDefault();
      alert("Please enter a task.");
    }
  });
});
