const registerBtn = document.querySelector("nav button");
const container = document.querySelector(".container");

registerBtn.addEventListener("click", () => {
    container.classList.add("animate");
});
