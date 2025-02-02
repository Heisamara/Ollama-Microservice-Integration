// Sidebar Toggle
const sidebar = document.querySelector(".sidebar");
const closeSidebarBtn = document.getElementById("close-sidebar");
const menuBtn = document.getElementById("menu-btn");

closeSidebarBtn.addEventListener("click", () => {
  sidebar.classList.add("hidden");
  menuBtn.style.display = "block";
});

menuBtn.addEventListener("click", () => {
  sidebar.classList.remove("hidden");
  menuBtn.style.display = "none";
});

// Dark Mode Toggle
document.getElementById("theme-toggle").addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
});
