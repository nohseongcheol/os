// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.Asli;

/** 표준 Java 오류를 Melayu API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class tukar_pengecualian {
    private tukar_pengecualian() {}
    public static I_O_pengecualian I_O(java.io.IOException RALAT) {
        if (RALAT instanceof I_O_pengecualian) return (I_O_pengecualian)RALAT;
        if (RALAT instanceof java.net.SocketTimeoutException) return new tunggu_TIMEOUT_pengecualian("통신 대기시간을 넘었습니다.");
        if (RALAT instanceof java.net.UnknownHostException) return new e_mel_Carian_pengecualian("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (RALAT instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 lajur_VALUE 수 없습니다.");
        if (RALAT instanceof java.net.SocketException) return new 통신예외("통신 Sambung 작업 kegagalan_VALUE: " + RALAT.getMessage());
        return new I_O_pengecualian("I_O 작업 kegagalan_VALUE: " + RALAT.getMessage());
    }
    public static RuntimeException laksanakan_perintah(RuntimeException RALAT) {
        if (RALAT instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (RALAT instanceof java.lang.IllegalArgumentException) return new tak_sah_argumen_pengecualian("인수의 값이나 범위를 확인하십시오.");
        if (RALAT instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (RALAT instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (RALAT instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (RALAT instanceof java.lang.NullPointerException) return new rujukan_nol_pengecualian("비어 있는 참조입니다.");
        return new 실행예외(RALAT.getMessage());
    }
}
