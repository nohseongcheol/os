// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;

/** 표준 Java 오류를 Slovenský API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERT_výnimka {
    private CONVERT_výnimka() {}
    public static vstup_a_výstup_výnimka vstup_a_výstup(java.io.IOException chyba) {
        if (chyba instanceof vstup_a_výstup_výnimka) return (vstup_a_výstup_výnimka)chyba;
        if (chyba instanceof java.net.SocketTimeoutException) return new počkaj_TIMEOUT_výnimka("통신 대기시간을 넘었습니다.");
        if (chyba instanceof java.net.UnknownHostException) return new adresa_LOOKUP_výnimka("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (chyba instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 COLUMN_VALUE 수 없습니다.");
        if (chyba instanceof java.net.SocketException) return new 통신예외("통신 Pripojiť 작업 zlyhanie_VALUE: " + chyba.getMessage());
        return new vstup_a_výstup_výnimka("vstup_a_výstup 작업 zlyhanie_VALUE: " + chyba.getMessage());
    }
    public static RuntimeException Vykonať_príkaz(RuntimeException chyba) {
        if (chyba instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (chyba instanceof java.lang.IllegalArgumentException) return new neplatné_argument_výnimka("인수의 값이나 범위를 확인하십시오.");
        if (chyba instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (chyba instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (chyba instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (chyba instanceof java.lang.NullPointerException) return new NEPLATNÝ_zdroj_výnimka("비어 있는 참조입니다.");
        return new 실행예외(chyba.getMessage());
    }
}
