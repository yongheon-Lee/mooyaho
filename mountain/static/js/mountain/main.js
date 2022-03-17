const clickedMountainImage = (e) => {
    const mountainId = e.target.parentElement.dataset.id;
    location.href = `mountains/detail/${mountainId}`;
}

const mountainImages = document.querySelectorAll('.image-wrapper');
mountainImages.forEach(mountainImage => {
    mountainImage.addEventListener('click', clickedMountainImage);
})