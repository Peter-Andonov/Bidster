const imgContainer = document.querySelector('.form__previews_container');
const imgInput = document.getElementById('id_images');

imgInput.addEventListener('change', (e) => {
    imgContainer.innerHTML = '';
    for (let i = 0; i < e.target.files.length; i++) {
        let preview = createImgContainer();
        preview.src = URL.createObjectURL(e.target.files[i]);
        imgContainer.appendChild(preview);
        preview.onload = () => {
            URL.revokeObjectURL(preview.src)
        }
    }
});

const createImgContainer = () => {
    let container = document.createElement("img");
    container.classList.add('form__image_preview');
    return container;
}