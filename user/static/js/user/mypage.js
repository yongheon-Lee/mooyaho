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

const clickedMyPhoto = () => {
    document.querySelector('#user-photo-changer').click();
}

const changeMyPhoto = (e) => {
    const csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
    const myPhotoElement = document.querySelector('#user-photo');
    const myPhoto = e.target.files[0];
    const formData = new FormData();
    formData.append('profile_img', myPhoto);
    
    $.ajax({
        type: 'POST',
        url: '/mypage/',
        processData: false,
        contentType: false,
        data: formData,
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        success: function(response){
            if (response['result'] == 'success'){
                const reader = new FileReader();
                reader.onload = function (e) {
                    myPhotoElement.setAttribute('src', e.target.result);
                }
                reader.readAsDataURL(myPhoto);
            }
            else {
                alert(response['msg'])
            }
        }
    })
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
document.querySelectorAll('#tab-area > div').forEach(element => {
    element.addEventListener('click', clickedTab);
})

document.querySelectorAll('.post-image-wrapper').forEach(element => {
    element.addEventListener('click', clickedPostImg);
})

document.querySelector('#img-wrapper > img').addEventListener('click', clickedMyPhoto);
document.querySelector('#icon-wrapper').addEventListener('click', clickedMyPhoto);
document.querySelector('#user-photo-changer').addEventListener('change', changeMyPhoto);

let observer;
document.addEventListener("DOMContentLoaded", function () {
    const intersectionObserverOptions = {
        root: null,
        rootMargin: '500px',
        threshold: 0
    }
    observer = new IntersectionObserver(afterMeetObserver, intersectionObserverOptions);
    let imgs = document.querySelectorAll('.post-image-wrapper > img');
    imgs.forEach(img => {
        observer.observe(img);
    })
});