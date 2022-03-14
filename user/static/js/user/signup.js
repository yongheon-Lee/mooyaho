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

const clickedSubmitBtn = (e) => {
    // 아이디 중복 체크 필요

    const pwInput = document.querySelector('#userPw');
    const pwInputConfirm = document.querySelector('#userPwConfirm');

    // 비밀번호 확인
    console.log(pwInputConfirm.value, pwInput.value);
    if (pwInputConfirm.value != pwInput.value) {
        e.preventDefault();
        e.stopPropagation();
        window.location.hash = '#userPwConfirm';
        pwInputConfirm.focus();
        return;
    }

    // 닉네임 중복 체크 필요

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

const clickedCancelBtn = (e) => {
    e.preventDefault();
    e.stopPropagation();
    location.href = '/login/';
}

const validatePwConfirm = (e) => {
    const pwInputVal = document.querySelector('#userPw').value;
    const pwInputConfirmVal = document.querySelector('#userPwConfirm').value;
    
    if (pwInputVal.length < 1) return;
    const confirmMsg = document.querySelector('#confirmMsg');
    console.dir(confirmMsg);
    if (pwInputConfirmVal === pwInputVal) {
        confirmMsg.style.color = 'RGB(0, 124, 76)';
        confirmMsg.textContent = '비밀번호와 동일 합니다';
    } else {
        confirmMsg.style.color = 'RGB(222, 45, 64)';
        confirmMsg.textContent = '비밀번호와 동일하지 않습니다';
    }
}

document.querySelector('#button-area > button:nth-child(1)').addEventListener('click', clickedSubmitBtn);
document.querySelector('#button-area > button:nth-child(2)').addEventListener('click', clickedCancelBtn);
document.querySelector('#userPwConfirm').addEventListener('input', validatePwConfirm);