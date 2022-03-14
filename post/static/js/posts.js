$(function() {
    changeSearchToAdd();
    console.log("loaded");
})

function changeSearchToAdd() {
    // img = document.getElementsByClassName("meterial-icons");
    const img1 = document.getElementById("search-wrapper");
    img1.innerHTML = `<button type="button" onclick="location.href='/posts/new'">글쓰기</button>`;

}