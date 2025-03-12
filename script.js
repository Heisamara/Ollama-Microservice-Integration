document.addEventListener("DOMContentLoaded", function () {
  const inputBox = document.querySelector(".input-box input");
  const sendButton = document.querySelector(".input-box button");
  const chatArea = document.querySelector(".chat-area");

  sendButton.addEventListener("click", async () => {
      const userInput = inputBox.value.trim();
      if (!userInput) return;

      // Display user message
      const userMessage = document.createElement("p");
      userMessage.textContent = `You: ${userInput}`;
      chatArea.appendChild(userMessage);
      inputBox.value = "";

      try {
          const response = await fetch("http://localhost:5000/generate", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ text: userInput })
          });

          if (!response.ok) {
              throw new Error("Failed to fetch response from server");
          }

          // Handle streaming response
          const reader = response.body.getReader();
          const decoder = new TextDecoder();
          let botMessage = document.createElement("p");
          botMessage.textContent = "Bot: ";
          chatArea.appendChild(botMessage);

          while (true) {
              const { done, value } = await reader.read();
              if (done) break;
              botMessage.textContent += decoder.decode(value, { stream: true });
          }
      } catch (error) {
          console.error("Error:", error);
          const errorMessage = document.createElement("p");
          errorMessage.textContent = "Error: Could not get response from AI.";
          chatArea.appendChild(errorMessage);
      }
  });

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
});

