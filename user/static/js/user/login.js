// csrf 토큰을 얻음
const getCsrfTokenElement = () => {
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0];
    const hiddenField = document.createElement("input");
    hiddenField.setAttribute("type", "hidden");
    hiddenField.setAttribute("name", csrfToken.name);
    hiddenField.setAttribute("value", csrfToken.value);
    return hiddenField;
}

// 동적 form(로그인) 요청
const submitDynamicForm = (loginInfo) => {
    const newForm = document.createElement('form');

    newForm.method = 'post';
    newForm.action = '/login/'

    for (const [key, value] of Object.entries(loginInfo)) {
        let inputElement = document.createElement('input');
        inputElement.setAttribute('type', 'hidden');
        inputElement.setAttribute('name', key);
        inputElement.setAttribute('value', value);
        newForm.appendChild(inputElement);
    }

    newForm.appendChild(getCsrfTokenElement());

    document.body.appendChild(newForm);
    newForm.submit();
}

// 로그인 요청
const requestLogin = () => {
    const inputInfo = {
        'email': document.querySelector('#email').value,
        'password': document.querySelector('#userPw').value,
        'latitude': latitude,
        'longitude': longitude,
    }
    submitDynamicForm(inputInfo);
}

// 로그인 or 회원가입 버튼 눌렀을 때
const clickedButton = (e) => {
    if (e.target.innerText == '로그인') {
        if (!checkBlankLoginInfo()) return;
        requestLogin();
    } else {
        location.href = '/signup';
    }
}

// 사용자 위치정보를 얻음
const getUserLocation = () => {
    if (!navigator.geolocation) {
        throw "위치 정보가 지원되지 않습니다.";
    }
    navigator.geolocation.getCurrentPosition(({coords}) => {
        latitude = coords.latitude // 위도
        longitude = coords.longitude; // 경도
    });
}

// 로그인 정보(이메일, 비밀번호) 공백인지 확인
const checkBlankLoginInfo = () => {
    const loginInfo = [
        document.querySelector('#email'),
        document.querySelector('#userPw')
    ]
    for (let index in loginInfo) {
        if (loginInfo[index].value == '') {
            document.querySelector('#error-msg-area > span').innerText = '이메일 혹은 비밀번호가 공백입니다.'
            loginInfo[index].focus();
            return false;
        }
    }
    return true;
}

// 키보드를 눌렀을 때
const afterKeyDown = (e) => {
    if (e.keyCode == 13) { // enter
        if (!checkBlankLoginInfo()) return;
        requestLogin();
    }
}

// 실행 부분
let latitude = 0;
let longitude = 0;
const buttons = document.querySelectorAll('#button-area > button');
for (let i=0; i<buttons.length; i++){
    buttons[i].addEventListener('click', clickedButton);
}

// 유저 위치 정보
getUserLocation();

// keyboard event
window.addEventListener('keydown', afterKeyDown);

// DOM 구성 후 
document.addEventListener("DOMContentLoaded", function () {
    document.querySelector('#email').focus();
});