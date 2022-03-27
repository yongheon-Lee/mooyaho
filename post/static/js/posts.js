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
$('.post_like').click(function () {
    // 해당 글 id 가져오기
    const pk = $(this).attr('id');

    // 비동기 통신 시작
    $.ajax({
        url: '/posts/' + pk + '/likes/',
        type: 'POST',
        data: {'pk': pk},
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        success: function (response) {
            $('#like_count-' + pk).html('좋아요&nbsp;' + response.likes_count + '개');
            if (response.message === '좋아요') {
                $('#like_heart' + pk).attr({'class': 'fas fa-heart', 'style': '#bd1f00'});
            } else if (response.message === '좋아요 취소') {
                $('#like_heart' + pk).attr({'class': 'far fa-heart', 'style': '#3d3d3d'});
            }
        },
        error: function (request, status, error) {
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
        'comment': comment,
        'post_id': pk
    }

    // 비동기 통신 시작
    $.ajax({
        url: '/posts/' + pk + '/comments/',
        type: 'POST',
        data: JSON.stringify(params),
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        success: function (data) {
            // 댓글 추가
            $('.comment-area').append(`
            <div style="display: flex; align-items: center; justify-content: space-around" class="comment-${data.comment_id}">
                <p>${data.author}</p>
                <p>${data.comment}</p>
                <input type="button" id="repleDeleteBtn" name="${data.post_id}"
                       onclick="repleDelete(${data.comment_id})" value="삭제">
            </div>`)
            // 댓글 입력창 내용 초기화
            $('#comments').val('');
        },
        error: function () {
            alert('오류가 발생했습니다!')
        }
    })
})

// 댓글 삭제 구현
function repleDelete(id) {
    // 삭제 승인 요청 메시지
    let delete_confirm = confirm('댓글을 삭제할까요?');
    // 삭제 승인 시
    if (delete_confirm === true) {
        // 해당 글 id 가져오기
        const pk = $('#repleDeleteBtn').attr('name');
        // 백엔드로 보낼 데이터 작성
        let params = {'comment_id': id}

        // 비동기 통신 시작
        $.ajax({
            url: '/posts/' + pk + '/comments/',
            type: 'DELETE',
            data: JSON.stringify(params),
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            },
            success: function (data) {
                console.log(data)
                if (data.result === 'ok') {
                    // 댓글 삭제 처리
                    $('.comment-'+id).remove();
                }
            },
            error: function () {
                alert('오류가 발생했습니다!')
            }
        })
    }
}

// 신고하기 구현
$('#reportBtn').click(function () {
    // 신고 요청 확인
    let report_confirm = confirm('이 글을 신고하시겠습니까?')
    // 신고 처리
    if (report_confirm === true) {
        // 해당 글 id 가져오기
        const pk = $(this).attr('name');
        // 신고자 가져오기
        let report_user = document.querySelector('#report-user').innerText;
        // 신고 내용 가져오기
        let content = document.querySelector('#contents').value;
        // 백엔드로 넘길 데이터 작성
        let params = {
            'author': report_user,
            'content': content,
        }

        // 비동기 통신 시작
        $.ajax({
            url: '/posts/' + pk + '/reports/',
            type: 'POST',
            data: JSON.stringify(params),
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            },
            success: function (data) {
                alert(data.author + '님의 신고를 접수했습니다.')
                // 신고 내용 입력창 내용 초기화
                $('#contents').val('');
                // 모달 정의
                const modal = document.querySelector(".modal");
                // 모달 닫기
                modal.style.display = 'none';
            },
            error: function () {
                alert('오류가 발생했습니다!');
            }
        })
    }
})