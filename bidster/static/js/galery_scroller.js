const leftArrow = document.querySelectorAll('.arrow__icon')[0];
const rightArrow = document.querySelectorAll('.arrow__icon')[1];
const focusImg = document.querySelectorAll('.details__galery_image')[0];
const imgPreviews = document.querySelectorAll(".details__galery_image_preview");
const imgPreviewsCounter = document.querySelector('.details__galery_image_counter');
let currentIdx = 0;

leftArrow.addEventListener("click", (e) => {
    if(currentIdx <= 0){
        return
    }

    currentIdx --;
    focusImg.src = imgPreviews[currentIdx].src
    updateCounter()
});


rightArrow.addEventListener("click", (e) => {
    if(currentIdx >= imgPreviews.length - 1){
        return
    }

    currentIdx ++;
    focusImg.src = imgPreviews[currentIdx].src
    updateCounter()
});

const updateCounter = () => {
    imgPreviewsCounter.innerText = `${currentIdx + 1}/${imgPreviews.length}`
}