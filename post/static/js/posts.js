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