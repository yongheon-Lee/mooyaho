
const clickedNavigateButton = (e) => {
    const url = e.target.dataset.url;
    if (url === '/logout/') {
        localStorage.removeItem('mountainNameList');
    }
    
    location.href = url;
}

const setMountainListToLocalStorage = () => {
    $.ajax({
        type: 'GET',
        url: '/get-mountain-list/',
        success: function(response){
            if (response['result'] == 'success'){
                localStorage.setItem('mountainNameList', response['mountains']);
            }
            else {
                alert('산 리스트를 가져오지 못했습니다');
            }
        }
    });
}

const addMountainListFromLocalStorage = () => {
    const mountainSearchOptions = document.querySelector('#datalistOptions');
    mountainNameList = localStorage.getItem('mountainNameList').split(',');
    mountainNameList.forEach(name => {
        let option = document.createElement('option');
        option.setAttribute('value', name);
        mountainSearchOptions.appendChild(option);
    });
}

const goSearchedMountainPage = (searchInput) => {
    const searchWord = searchInput.children[0].value;
    const searchIndex = mountainNameList.indexOf(searchWord) + 1;
    if (searchIndex == 0) {
        alert('검색 할 수 없는 산 입니다');
        return;
    }
    if (searchWord != '') {
        location.href = `/mountains_detail/${searchIndex}`;
    }
}

const clickedSearchButton = (e) => {
    const headerElement = e.target.parentElement.parentElement;
    const searchInput = headerElement.children[3];

    if (searchInput.classList.length == 1) { // 검색창이 안 보인다면
        if (localStorage.getItem('mountainNameList') === null) {
            setMountainListToLocalStorage();
        } 
        addMountainListFromLocalStorage();
        
        for (let i=0; i<headerElement.children.length-1; i++){
            headerElement.children[i].classList.toggle('hide');
        }
        searchInput.children[0].focus();
    } else {
        goSearchedMountainPage(searchInput);
    }
}

const enterSearch = (e) => {
    if (e.keyCode == 13) { // enter
        const searchInput = document.querySelector('#search-input');
        if (document.activeElement == searchInput.children[0]) { // 검색창이 focus인 경우에만 검색 요청 시도
            goSearchedMountainPage(searchInput);
        }
    }
}

const clickedSearchBackButton = (e) => {
    const headerElement = e.target.parentElement.parentElement;
    for (let i=0; i<headerElement.children.length-1; i++){
        headerElement.children[i].classList.toggle('hide');
    }
    document.querySelector('#mountainSearchBar').value = '';
}

// 실행부
let mountainNameList;
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
window.addEventListener('keydown', enterSearch);