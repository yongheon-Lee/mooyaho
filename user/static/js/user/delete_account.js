// 회원 탈퇴 구현
$('#complete-btn').click(function (){
    // 탈퇴 요청 확인
    let delete_confirm = confirm('탈퇴 하시겠습니까?');

    // 탈퇴 처리
    if (delete_confirm === true){
        // 신고 내용 가져오기
        let delete_reason = document.querySelector('#deleteReason').value;

        // 백엔드로 넘길 데이터 작성
        let params = {
            'delete_reason': delete_reason,
        }

        // 비동기 통신 시작
        $.ajax({
            url: '/delete-account/',
            type: 'POST',
            data: JSON.stringify(params),
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
            },
            success: function (data) {
                if (data.result === 'ok'){
                    alert('탈퇴 처리가 완료됐습니다. 이용해 주셔서 감사합니다.');
                    window.location = '/login/';
                }
            },
            error: function (request, status, error){
                alert('오류가 발생했습니다!');
            }
        })
    }
})