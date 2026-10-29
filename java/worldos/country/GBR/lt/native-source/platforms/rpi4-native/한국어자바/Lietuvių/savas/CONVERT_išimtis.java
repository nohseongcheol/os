// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;

/** 표준 Java 오류를 Lietuvių API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERT_išimtis {
    private CONVERT_išimtis() {}
    public static Į_I_išimtis Į_I(java.io.IOException KLAIDA) {
        if (KLAIDA instanceof Į_I_išimtis) return (Į_I_išimtis)KLAIDA;
        if (KLAIDA instanceof java.net.SocketTimeoutException) return new Palauk_SKIRTASIS_LAIKAS_išimtis("통신 대기시간을 넘었습니다.");
        if (KLAIDA instanceof java.net.UnknownHostException) return new ADDRESS_LOOKUP_išimtis("주소를 확인할 numeris 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (KLAIDA instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 COLUMN_VALUE numeris 없습니다.");
        if (KLAIDA instanceof java.net.SocketException) return new 통신예외("통신 Prisijungti 작업 triktis_VALUE: " + KLAIDA.getMessage());
        return new Į_I_išimtis("Į_I 작업 triktis_VALUE: " + KLAIDA.getMessage());
    }
    public static RuntimeException Vykdyti_komanda(RuntimeException KLAIDA) {
        if (KLAIDA instanceof java.lang.NumberFormatException) return new numeris_formatas_triktis("숫자의 형식이나 범위를 확인하십시오.");
        if (KLAIDA instanceof java.lang.IllegalArgumentException) return new neleistinas_argumentas_išimtis("인수의 값이나 범위를 확인하십시오.");
        if (KLAIDA instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (KLAIDA instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (KLAIDA instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (KLAIDA instanceof java.lang.NullPointerException) return new NULL_nuoroda_išimtis("비어 있는 참조입니다.");
        return new 실행예외(KLAIDA.getMessage());
    }
}
