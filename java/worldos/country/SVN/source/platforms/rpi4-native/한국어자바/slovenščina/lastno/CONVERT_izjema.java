// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;

/** 표준 Java 오류를 slovenščina API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERT_izjema {
    private CONVERT_izjema() {}
    public static V_I_izjema V_I(java.io.IOException NAPAKA) {
        if (NAPAKA instanceof V_I_izjema) return (V_I_izjema)NAPAKA;
        if (NAPAKA instanceof java.net.SocketTimeoutException) return new počakaj_TIMEOUT_izjema("통신 대기시간을 넘었습니다.");
        if (NAPAKA instanceof java.net.UnknownHostException) return new naslov_LOOKUP_izjema("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (NAPAKA instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 COLUMN_VALUE 수 없습니다.");
        if (NAPAKA instanceof java.net.SocketException) return new 통신예외("통신 Poveži 작업 napaka_VALUE: " + NAPAKA.getMessage());
        return new V_I_izjema("V_I 작업 napaka_VALUE: " + NAPAKA.getMessage());
    }
    public static RuntimeException Izvedi_ukaz(RuntimeException NAPAKA) {
        if (NAPAKA instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (NAPAKA instanceof java.lang.IllegalArgumentException) return new neveljaven_argument_izjema("인수의 값이나 범위를 확인하십시오.");
        if (NAPAKA instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (NAPAKA instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (NAPAKA instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (NAPAKA instanceof java.lang.NullPointerException) return new NULL_Gradiva_izjema("비어 있는 참조입니다.");
        return new 실행예외(NAPAKA.getMessage());
    }
}
