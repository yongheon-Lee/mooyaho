
const clickedNavigateButton = (e) => {
    location.href = e.target.dataset.url;
}

const clickedSearchButton = (e) => {
    const headerElement = e.target.parentElement.parentElement;
    const searchInput = headerElement.children[3];
    if (searchInput.classList.length == 1) { // 검색창이 안 보인다면
        for (let i=0; i<headerElement.children.length-1; i++){
            headerElement.children[i].classList.toggle('hide');
        }
    } else {
        const searchWord = searchInput.children[0].value;
        if (searchWord != '') {
            location.href = `/search?word=${searchWord}`;
        }
    }
}

const clickedSearchBackButton = (e) => {
    const headerElement = e.target.parentElement.parentElement;
    for (let i=0; i<headerElement.children.length-1; i++){
        headerElement.children[i].classList.toggle('hide');
    }
}

// 실행부
const menuButtons = document.querySelectorAll('#menu-btn-group > button');
for(let i=0; i<menuButtons.length; i++) {
    menuButtons[i].addEventListener('click', clickedNavigateButton);
}

const footerButtons = document.querySelectorAll('.footer-button-wrapper > i');
for(let i=0; i<footerButtons.length; i++) {
    footerButtons[i].addEventListener('click', clickedNavigateButton);
}

document.querySelector('#search-wrapper').addEventListener('click', clickedSearchButton);
document.querySelector('#search-back-wrapper').addEventListener('click', clickedSearchBackButton);