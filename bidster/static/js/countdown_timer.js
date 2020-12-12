const elements = document.querySelectorAll('.has_counter');

elements.forEach((e) =>{
    const expiryDateEl = e.querySelector('.expiry_date');
    const counterEl = e.querySelector('.counter');

    let countDownDate = new Date(expiryDateEl.innerText).getTime();

    let x = setInterval(() => {

        let now = new Date().getTime();

        let distance = countDownDate - now;

        let days = Math.floor(distance / (1000 * 60 * 60 * 24));
        let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        let seconds = Math.floor((distance % (1000 * 60)) / 1000);

        counterEl.innerText = days + "d " + hours + "h " + minutes + "m " + seconds + "s Remaining";

        if (distance < 0) {
            counterEl.innerText = "EXPIRED";
            counterEl.classList.add('expired');
            clearInterval(x);
        }
    }, 1000);
});
