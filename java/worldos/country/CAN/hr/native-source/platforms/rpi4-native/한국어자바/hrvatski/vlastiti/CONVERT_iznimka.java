// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;

/** 표준 Java 오류를 hrvatski API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERT_iznimka {
    private CONVERT_iznimka() {}
    public static U_I_iznimka U_I(java.io.IOException GREŠKA) {
        if (GREŠKA instanceof U_I_iznimka) return (U_I_iznimka)GREŠKA;
        if (GREŠKA instanceof java.net.SocketTimeoutException) return new čekaj_TIMEOUT_iznimka("통신 대기시간을 넘었습니다.");
        if (GREŠKA instanceof java.net.UnknownHostException) return new adresa_LOOKUP_iznimka("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (GREŠKA instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 COLUMN_VALUE 수 없습니다.");
        if (GREŠKA instanceof java.net.SocketException) return new 통신예외("통신 Spoji_se 작업 kvar_VALUE: " + GREŠKA.getMessage());
        return new U_I_iznimka("U_I 작업 kvar_VALUE: " + GREŠKA.getMessage());
    }
    public static RuntimeException Izvrši_naredba(RuntimeException GREŠKA) {
        if (GREŠKA instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (GREŠKA instanceof java.lang.IllegalArgumentException) return new nevaljan_argument_iznimka("인수의 값이나 범위를 확인하십시오.");
        if (GREŠKA instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (GREŠKA instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (GREŠKA instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (GREŠKA instanceof java.lang.NullPointerException) return new NULL_Reference_iznimka("비어 있는 참조입니다.");
        return new 실행예외(GREŠKA.getMessage());
    }
}
