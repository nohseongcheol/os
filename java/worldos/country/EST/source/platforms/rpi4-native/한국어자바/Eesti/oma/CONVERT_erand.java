// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;

/** 표준 Java 오류를 Eesti API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERT_erand {
    private CONVERT_erand() {}
    public static I_O_erand I_O(java.io.IOException VIGA) {
        if (VIGA instanceof I_O_erand) return (I_O_erand)VIGA;
        if (VIGA instanceof java.net.SocketTimeoutException) return new Oota_TIMEOUT_erand("통신 대기시간을 넘었습니다.");
        if (VIGA instanceof java.net.UnknownHostException) return new ADDRESS_LOOKUP_erand("주소를 확인할 number 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (VIGA instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 veerg_VALUE number 없습니다.");
        if (VIGA instanceof java.net.SocketException) return new 통신예외("통신 Ühendu 작업 tõrge_VALUE: " + VIGA.getMessage());
        return new I_O_erand("I_O 작업 tõrge_VALUE: " + VIGA.getMessage());
    }
    public static RuntimeException Täida_käsk(RuntimeException VIGA) {
        if (VIGA instanceof java.lang.NumberFormatException) return new number_vorming_tõrge("숫자의 형식이나 범위를 확인하십시오.");
        if (VIGA instanceof java.lang.IllegalArgumentException) return new kehtetu_argument_erand("인수의 값이나 범위를 확인하십시오.");
        if (VIGA instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (VIGA instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (VIGA instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (VIGA instanceof java.lang.NullPointerException) return new NULL_viide_erand("비어 있는 참조입니다.");
        return new 실행예외(VIGA.getMessage());
    }
}
