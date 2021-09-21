window.addEventListener("scroll", () => {
    const header = document.querySelector('header');
    header.classList.toggle('sticky', window.scrollY > 0);
});

const navigation = document.querySelector('nav');
const toggle = document.querySelector('.toggle');
toggle.onclick = () => {
    toggle.classList.toggle('active');
    navigation.classList.toggle('active');
}