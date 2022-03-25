$(function () {
    changeSearchToAdd();
})

function changeSearchToAdd() {
    // img = document.getElementsByClassName("meterial-icons");
    const img1 = document.getElementById("search-wrapper");
    img1.removeEventListener('click', clickedSearchButton);
    img1.innerHTML = `<button type="button" onclick="location.href='/posts/new'">글쓰기</button>`;
}

function modalReport() {
    const modal = document.querySelector(".modal");
    modal.style.display = 'block';
}

function modalClose() {
    const modal = document.querySelector(".modal");
    const closeBtn = document.querySelector("#modalClose");
    modal.style.display = 'none';
}

// 좋아요 구현(참고 자료: https://wonjongah.tistory.com/41)
// csrf 토큰 가져오기
const csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
$('.post_like').click(function (){
    // 해당 글 id 가져오기
    const pk = $(this).attr('name');

    // 비동기 통신 시작
    $.ajax({
        url: '/posts/'+ pk +'/likes/',
        type: 'POST',
        data: {'pk': pk},
        dataType: 'json',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        success: function (response){
            $('#like_count-'+ pk).html('좋아요&nbsp;' + response.likes_count + '개');
            if (response.message === '좋아요'){
                $('#like_heart' + pk).attr('class', 'fas fa-heart')
            } else if (response.message === '좋아요 취소'){
                $('#like_heart' + pk).attr('class', 'far fa-heart')
            }
        },
        error: function (request, status, error){
            alert('오류가 발생했습니다!')
        }
    })
})

// 댓글 작성 구현
$('#repleBtn').click(function () {
    // 해당 글 id 가져오기
    const pk = $(this).attr('name');
    // 댓글 작성자 가져오기
    let author = document.querySelector('#author').innerText;
    // 댓글 내용 가져오기
    let comment = document.querySelector('#comments').value;
    // 백엔드로 넘길 데이터 작성
    let params = {
        'author': author,
        'comment': comment
    }

    // 비동기 통신 시작
    $.ajax({
        url: '/posts/' + pk + '/comments/',
        type: 'POST',
        data: JSON.stringify(params),
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        success: function (data){
            console.log(data)
            $('.comment-area').append(`
            <div style="display: flex; align-items: center; justify-content: space-around">
                <p>${data.author}</p>
                <p>${data.comment}</p>
                <button>삭제</button>
            </div>`)
        },
        error: function (){
            alert('오류가 발생했습니다!')
        }
    })
})

// 댓글 삭제 구현
function repleDelete(id){
    // 해당 글 id 가져오기
    const pk = $('#repleDeleteBtn').attr('name');
    console.log(pk)
    // 백엔드로 보낼 데이터 작성
    let params = {'comment_id': id}

    // 비동기 통신 시작
    $.ajax({
        url: '/posts/' + pk + '/comments/deletion/',
        type: 'POST',
        data: JSON.stringify(params),
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        success: function (data){
            console.log(data)
            let comment_id = data.comment_id
            if (data.result === 'ok'){
                $('#comment-' + comment_id).remove(); // 안되는 것 같습니다.....
                alert('삭제했습니다.')
            }
        },
        error: function (){
            alert('오류가 발생했습니다!')
        }
    })
}

// 신고하기 구현
$('#reportBtn').click(function () {
    // 해당 글 id 가져오기
    const pk = $(this).attr('name');
    // 신고자 가져오기
    let report_user = document.querySelector('#report-user').innerText;
    // 신고 내용 가져오기
    let content = document.querySelector('#contents').value;
    // 백엔드로 넘길 데이터 작성
    let params = {
        'author': report_user,
        'content': content
    }

    // 비동기 통신 시작
    $.ajax({
        url: '/posts/' + pk + '/reports/',
        type: 'POST',
        data: JSON.stringify(params),
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        success: function (data){
            alert('신고를 접수했습니다.')
            console.log(data);
            $('#content').val('');
        },
        error: function (){
            alert('오류가 발생했습니다!');
        }
    })
})