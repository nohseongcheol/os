// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 표준 Java 오류를 한국어 API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERT_unntak {
    private CONVERT_unntak() {}
    public static I_U_unntak I_U(java.io.IOException FEIL) {
        if (FEIL instanceof I_U_unntak) return (I_U_unntak)FEIL;
        if (FEIL instanceof java.net.SocketTimeoutException) return new vent_TIMEOUT_unntak("통신 대기시간을 넘었습니다.");
        if (FEIL instanceof java.net.UnknownHostException) return new ADDRESS_LOOKUP_unntak("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (FEIL instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 COLUMN_VALUE 수 없습니다.");
        if (FEIL instanceof java.net.SocketException) return new 통신예외("통신 Kopla_til 작업 feil_VALUE: " + FEIL.getMessage());
        return new I_U_unntak("I_U 작업 feil_VALUE: " + FEIL.getMessage());
    }
    public static RuntimeException Utfør_kommando(RuntimeException FEIL) {
        if (FEIL instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (FEIL instanceof java.lang.IllegalArgumentException) return new ugyldig_argument_unntak("인수의 값이나 범위를 확인하십시오.");
        if (FEIL instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (FEIL instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (FEIL instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (FEIL instanceof java.lang.NullPointerException) return new NULL_Oppslagsverk_unntak("비어 있는 참조입니다.");
        return new 실행예외(FEIL.getMessage());
    }
}
