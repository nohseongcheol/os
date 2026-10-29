// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 표준 Java 오류를 한국어 API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERT_istisna {
    private CONVERT_istisna() {}
    public static giriş_çıxış_istisna giriş_çıxış(java.io.IOException XƏTA) {
        if (XƏTA instanceof giriş_çıxış_istisna) return (giriş_çıxış_istisna)XƏTA;
        if (XƏTA instanceof java.net.SocketTimeoutException) return new gözlə_FASİLƏ_istisna("통신 대기시간을 넘었습니다.");
        if (XƏTA instanceof java.net.UnknownHostException) return new ünvan_LOOKUP_istisna("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (XƏTA instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 sütun_VALUE 수 없습니다.");
        if (XƏTA instanceof java.net.SocketException) return new 통신예외("통신 Bağlan 작업 xəta_VALUE: " + XƏTA.getMessage());
        return new giriş_çıxış_istisna("giriş_çıxış 작업 xəta_VALUE: " + XƏTA.getMessage());
    }
    public static RuntimeException icra_etmək_əmr(RuntimeException XƏTA) {
        if (XƏTA instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (XƏTA instanceof java.lang.IllegalArgumentException) return new yanlış_arqument_istisna("인수의 값이나 범위를 확인하십시오.");
        if (XƏTA instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (XƏTA instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (XƏTA instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (XƏTA instanceof java.lang.NullPointerException) return new NULL_İstinad_istisna("비어 있는 참조입니다.");
        return new 실행예외(XƏTA.getMessage());
    }
}
