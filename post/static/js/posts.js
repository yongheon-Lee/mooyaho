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

// 좋아요 구현
// 참고 자료: https://wonjongah.tistory.com/41
const csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
$('.post_like').click(function (){
    const pk = $(this).attr('name')
    $.ajax({
        url: '/posts/'+ pk +'/likes/',
        type: 'post',
        data: {'pk': pk},
        dataType: 'json',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        success: function (response){
            alert(response.message)
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

// 댓글 구현
let repleBtn = document.querySelector('.repleBtn');
repleBtn.addEventListener('click', e => {
    let comment = document.querySelector('#comments').value;
    let params = {
        'author': '{{ request.user.nickname }}',
        'post': '{{ post.id }}',
        'comment': comment
    }
    console.log(params)

    $.ajax({
        url: "/comments/",
        type: 'POST',
        headers: {
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        },
        data: JSON.stringify(params),
        success: function (data){
            console.log(data)
        },
        error: function (){
            alert('Nope!!!!!!!!!!!')
        }
    })
})