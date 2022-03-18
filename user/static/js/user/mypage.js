const clickedTab = (e) => {
    document.querySelectorAll('#tab-area > div').forEach(element => {
        element.classList.toggle('active');
    })
    document.querySelectorAll('.tab-area-content').forEach(element => {
        element.classList.toggle('hide');
    })
}

const clickedPostImg = (e) => {
    const postId = e.target.parentElement.dataset.id;
    if (postId == undefined) return;
    location.href = `/posts/${postId}`;
}

document.querySelectorAll('#tab-area > div').forEach(element => {
    element.addEventListener('click', clickedTab);
})

document.querySelectorAll('.post-image-wrapper').forEach(element => {
    element.addEventListener('click', clickedPostImg);
})