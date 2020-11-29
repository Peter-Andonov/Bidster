const imgContainer = document.querySelector('.form__previews_container');
const imgInput = document.querySelector('.form__image_input');

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
    return container;
}