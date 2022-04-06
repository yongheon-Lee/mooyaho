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

// 회원 탈퇴 구현
$('#complete-btn').click(function (){
    // 탈퇴 요청 확인
    let delete_confirm = confirm('탈퇴 하시겠습니까?');

    // 탈퇴 처리
    if (delete_confirm === true){
        // 신고 내용 가져오기
        let delete_reason = document.querySelector('#deleteReason').value;

        // 백엔드로 넘길 데이터 작성
        let params = {
            'delete_reason': delete_reason,
        }

        // 비동기 통신 시작
        $.ajax({
            url: '/delete-account/',
            type: 'POST',
            data: JSON.stringify(params),
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
            },
            success: function (data) {
                if (data.result === 'ok'){
                    alert('탈퇴 처리가 완료됐습니다. 이용해 주셔서 감사합니다.');
                    window.location = '/login/';
                }
            },
            error: function (request, status, error){
                alert('오류가 발생했습니다!');
            }
        })
    }
})