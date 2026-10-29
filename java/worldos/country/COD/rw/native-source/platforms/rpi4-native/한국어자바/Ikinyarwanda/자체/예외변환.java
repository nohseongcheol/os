// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ikinyarwanda.자체;

/** 표준 Java 오류를 Ikinyarwanda API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class 예외변환 {
    private 예외변환() {}
    public static 입출력예외 I_O(java.io.IOException IKOSA) {
        if (IKOSA instanceof 입출력예외) return (입출력예외)IKOSA;
        if (IKOSA instanceof java.net.SocketTimeoutException) return new 대기시간초과예외("통신 대기시간을 넘었습니다.");
        if (IKOSA instanceof java.net.UnknownHostException) return new 주소확인예외("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (IKOSA instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 inkingi_agaciro 수 없습니다.");
        if (IKOSA instanceof java.net.SocketException) return new 통신예외("통신 Guhuza 작업 kudakora_agaciro: " + IKOSA.getMessage());
        return new 입출력예외("I_O 작업 kudakora_agaciro: " + IKOSA.getMessage());
    }
    public static RuntimeException gukora_ibwiriza(RuntimeException IKOSA) {
        if (IKOSA instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (IKOSA instanceof java.lang.IllegalArgumentException) return new 잘못된인수예외("인수의 값이나 범위를 확인하십시오.");
        if (IKOSA instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (IKOSA instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (IKOSA instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (IKOSA instanceof java.lang.NullPointerException) return new 빈참조예외("비어 있는 참조입니다.");
        return new 실행예외(IKOSA.getMessage());
    }
}
