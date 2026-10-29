// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 표준 Java 오류를 한국어 API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class 예외변환 {
    private 예외변환() {}
    public static ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ ໄອ_ໂອ(java.io.IOException ຂໍ້ຜິດພາດ) {
        if (ຂໍ້ຜິດພາດ instanceof ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ) return (ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ)ຂໍ້ຜິດພາດ;
        if (ຂໍ້ຜິດພາດ instanceof java.net.SocketTimeoutException) return new 대기시간초과예외("통신 대기시간을 넘었습니다.");
        if (ຂໍ້ຜິດພາດ instanceof java.net.UnknownHostException) return new ອີເມວ_ຄົ້ນຫາ_ຂໍ້ຍົກເວັ້ນ("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (ຂໍ້ຜິດພາດ instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 ຖັນ_ຄ່າ 수 없습니다.");
        if (ຂໍ້ຜິດພາດ instanceof java.net.SocketException) return new 통신예외("통신 ເຊື່ອມຕໍ່ 작업 ຫຼົ້ມເຫຼວ_ຄ່າ: " + ຂໍ້ຜິດພາດ.getMessage());
        return new ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ("ໄອ_ໂອ 작업 ຫຼົ້ມເຫຼວ_ຄ່າ: " + ຂໍ້ຜິດພາດ.getMessage());
    }
    public static RuntimeException ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(RuntimeException ຂໍ້ຜິດພາດ) {
        if (ຂໍ້ຜິດພາດ instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (ຂໍ້ຜິດພາດ instanceof java.lang.IllegalArgumentException) return new ໃຊ້ບໍ່ໄດ້_ຂໍ້ພິສູດ_ຂໍ້ຍົກເວັ້ນ("인수의 값이나 범위를 확인하십시오.");
        if (ຂໍ້ຜິດພາດ instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (ຂໍ້ຜິດພາດ instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (ຂໍ້ຜິດພາດ instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (ຂໍ້ຜິດພາດ instanceof java.lang.NullPointerException) return new ບໍ່ມີຄ່າ_ການ_ອ້າງ_ອີງ_ຂໍ້ຍົກເວັ້ນ("비어 있는 참조입니다.");
        return new 실행예외(ຂໍ້ຜິດພາດ.getMessage());
    }
}
