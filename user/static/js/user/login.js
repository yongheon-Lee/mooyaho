const getCsrfTokenElement = () => {
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0];
    const hiddenField = document.createElement("input");
    hiddenField.setAttribute("type", "hidden");
    hiddenField.setAttribute("name", csrfToken.name);
    hiddenField.setAttribute("value", csrfToken.value);
    return hiddenField;
}

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

const clickedButton = (e) => {
    if (e.target.innerText == '로그인') {
        const inputInfo = {
            'email': document.querySelector('#email').value,
            'password': document.querySelector('#userPw').value,
            'latitude': latitude,
            'longitude': longitude,
        }
        submitDynamicForm(inputInfo);
    } else {
        location.href = '/signup';
    }
}

const getUserLocation = () => {
    if (!navigator.geolocation) {
        throw "위치 정보가 지원되지 않습니다.";
    }
    navigator.geolocation.getCurrentPosition(({coords}) => {
        latitude = coords.latitude // 위도
        longitude = coords.longitude; // 경도
    });
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