const goMountainPage = (e) => {
    const id = e.target.parentElement.dataset.id;
    location.href = `/mountains_detail/${id}`;
};

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
document.querySelectorAll('.image-wrapper').forEach(mountainImg => {
    mountainImg.addEventListener('click', goMountainPage);
})

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
