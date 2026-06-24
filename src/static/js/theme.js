document.addEventListener("DOMContentLoaded", function () {
    const html = document.documentElement;
    const checkbox = document.querySelector("#themeToggle input[type='checkbox']");
    const savedTheme = localStorage.getItem("theme") || "light";

    html.setAttribute("data-bs-theme", savedTheme);
    checkbox.checked = savedTheme === "dark";

    checkbox.addEventListener("change", function () {
        const newTheme = checkbox.checked ? "dark" : "light";
        html.setAttribute("data-bs-theme", newTheme);
        localStorage.setItem("theme", newTheme);
    });
});