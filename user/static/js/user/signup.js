// 설문조사 검증
const validateSurvey = (e, groupInfo) => {
    let isPass = true;
    const groupInput = document.querySelectorAll(`input[name=${groupInfo.name}]:checked`);
    if (groupInput.length < 1) {
        e.preventDefault();
        e.stopPropagation();
        alert(`${groupInfo.msg} 선택해주세요!`);
        window.location.hash = `#${groupInfo.id}`;
        isPass = false;
    }
    return isPass;
}

// 가입 버튼 눌렀을 때
const clickedSubmitBtn = (e) => {
    document.querySelectorAll('.form-control').forEach(writeInput => {
        if (!writeInput.classList.contains('is-valid')) {
            e.preventDefault();
            e.stopPropagation();
            writeInput.focus();
            return;
        }
    })

    // 성별 체크 확인
    let groupInfo = {'name':'gender', 'msg':'성별을', 'id':'gender-area'}
    if (!validateSurvey(e, groupInfo)) return;

    // 연령대 체크 확인
    groupInfo = {'name':'age_gr', 'msg':'연령대를', 'id':'age-area'}
    if (!validateSurvey(e, groupInfo)) return;
    
    // 등산경력 체크 확인
    groupInfo = {'name':'exp', 'msg':'등산경력을', 'id':'exp-area'}
    if (!validateSurvey(e, groupInfo)) return;

    // 등산목적 체크 확인
    groupInfo = {'name':'reason', 'msg':'등산목적을', 'id':'reason-area'}
    if (!validateSurvey(e, groupInfo)) return;
}

// 취소 버튼 눌렀을 때
const clickedCancelBtn = (e) => {
    e.preventDefault();
    e.stopPropagation();
    location.href = '/login/';
}

// 입력 필드 검증 결과 표시
const showValidationResult = (valid, targetElement, msg, msgOn=true) => {
    const feedbackElement = valid ? targetElement.parentElement.children[2] : targetElement.parentElement.children[3]; 
    feedbackElement.textContent = msgOn ? msg : '';

    if (valid) {
        targetElement.classList.remove('is-invalid');
        targetElement.classList.add('is-valid');
    } else {
        targetElement.classList.remove('is-valid');
        targetElement.classList.add('is-invalid');
    }
}

// 이메일 형식 검증
const checkEmailValidation = (emailInputElement) => {
    let result = true;
    let msg = '좋아요:)';
    const emailRegExp = /^[A-Za-z0-9_]+[A-Za-z0-9]*[@]{1}[A-Za-z0-9]+[A-Za-z0-9]*[.]{1}[A-Za-z]{1,3}$/;
    if (!emailRegExp.test(emailInputElement.value)) {
        msg = '이메일 형식을 확인해주세요';
        showValidationResult(false, emailInputElement, msg);
        result =  false;
    } else {
        showValidationResult(true, emailInputElement, msg, false);
    }
    return result;
}

// 이메일 & 닉네임 중복 검증
const checkDuplication = (inputElement) => {
    const csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
    let msg = '좋아요:)';
    const requestData = {
        'type': inputElement.name,
        'data': inputElement.value
    }
    
    $.ajax({
        type: 'POST',
        url: '/signup/doublecheck/',
        dataType: 'json',
        data: JSON.stringify(requestData),
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        success: function(response){
            if (response['result']){
                showValidationResult(true, inputElement, msg);
            }
            else {
                msg = '중복 입니다.';
                showValidationResult(false, inputElement, msg);
            }
        },
        error: function(request, status, error) {
            msg = '죄송합니다. 중복 체크를 할 수 없습니다.';
            showValidationResult(false, inputElement, msg);
        }
    });
}

// 공백 검증
const checkBlank = (inputElement) => {
    result = true;
    let msg = '좋아요:)';
    if (inputElement.value === '') {
        msg = '공백 입니다.';
        showValidationResult(false, inputElement, msg);
        result = false;
    } else {
        showValidationResult(true, inputElement, msg);
    }
    return result;
}

// 비밀번호 & 비밀번호 확인 검증
const checkPwConfirm = (inputElement) => {
    const pwInputVal = document.querySelector('#userPw').value;
    const pwInputConfirmVal = document.querySelector('#userPwConfirm').value;
    let msg = '좋아요:)';
    result = true;
    
    if (pwInputVal.length < 1) return;
    
    if (pwInputConfirmVal === pwInputVal) {
        showValidationResult(true, inputElement, msg);
    } else {
        msg = '비밀번호가 일치하지 않습니다.';
        showValidationResult(false, inputElement, msg);
        result = false;
    }
    return result;
}

// 특수문자 유무 확인
const checkSpecialCharacter = (inputElement) => {
    const checkSpc = /[~!@#$%^&*()_+|<>?:{}]/;
    let msg = '좋아요:)';
    result = true;
    if (!checkSpc.test(inputElement.value)) {
        showValidationResult(true, inputElement, msg);
    } else {
        msg = '특수문자 포함 할 수 없습니다.';
        showValidationResult(false, inputElement, msg);
        result = false;
    }
    return result;
}

// 입력 필드 검증
const checkWriteInputValidation = (targetElement) => {
    const inputFieldName = targetElement.name;
    if (inputFieldName === 'email') {
        if(!checkBlank(targetElement)) return;
        if(!checkEmailValidation(targetElement)) return;
        checkDuplication(targetElement);
    } else if (inputFieldName === 'password') {
        if(!checkBlank(targetElement)) return;
    } else if (inputFieldName === 'password_confirm') {
        if(!checkBlank(targetElement)) return;
        if(!checkPwConfirm(targetElement)) return;
    } else if (inputFieldName === 'nickname') {
        if(!checkBlank(targetElement)) return;
        if(!checkSpecialCharacter(targetElement)) return;
        checkDuplication(targetElement);
    }
}

// 입력 필드 포커스아웃 되었을 때
const focusOutInputElement = (e) => {
    const focusoutElement = e.target;
    checkWriteInputValidation(focusoutElement);
}

document.querySelector('#button-area > button:nth-child(1)').addEventListener('click', clickedSubmitBtn);
document.querySelector('#button-area > button:nth-child(2)').addEventListener('click', clickedCancelBtn);
document.querySelectorAll('.form-control').forEach(inputEle => {
    inputEle.addEventListener('focusout', focusOutInputElement);
})