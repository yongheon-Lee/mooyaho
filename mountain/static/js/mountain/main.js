const clickedMountainImage = (e) => {
    const mountainId = e.target.parentElement.dataset.id;
    location.href = `mountains_detail/${mountainId}`;
}

const afterMeetObserver = (entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            let imgElement = entry.target;
            imgElement.setAttribute('src', imgElement.dataset.src);
            observer.unobserve(imgElement);
        }
    })
}

// 실행부
let observer;
document.addEventListener("DOMContentLoaded", function () {
    const intersectionObserverOptions = {
        root: null,
        rootMargin: '500px',
        threshold: 0
    }
    observer = new IntersectionObserver(afterMeetObserver, intersectionObserverOptions);
    let imgs = document.querySelectorAll('.image-wrapper > img');
    imgs.forEach(img => {
        observer.observe(img);
    })
});

const mountainImages = document.querySelectorAll('.image-wrapper');
mountainImages.forEach(mountainImage => {
    mountainImage.addEventListener('click', clickedMountainImage);
})

