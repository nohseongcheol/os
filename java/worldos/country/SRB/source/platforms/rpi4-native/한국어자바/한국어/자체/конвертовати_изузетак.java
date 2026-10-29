// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 표준 Java 오류를 한국어 API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class конвертовати_изузетак {
    private конвертовати_изузетак() {}
    public static У_И_изузетак У_И(java.io.IOException ГРЕШКА) {
        if (ГРЕШКА instanceof У_И_изузетак) return (У_И_изузетак)ГРЕШКА;
        if (ГРЕШКА instanceof java.net.SocketTimeoutException) return new 대기시간초과예외("통신 대기시간을 넘었습니다.");
        if (ГРЕШКА instanceof java.net.UnknownHostException) return new адреса_Претрага_изузетак("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (ГРЕШКА instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 колона_вриједност 수 없습니다.");
        if (ГРЕШКА instanceof java.net.SocketException) return new 통신예외("통신 Повежи_се 작업 неуспјех_вриједност: " + ГРЕШКА.getMessage());
        return new У_И_изузетак("У_И 작업 неуспјех_вриједност: " + ГРЕШКА.getMessage());
    }
    public static RuntimeException Изврши_команда(RuntimeException ГРЕШКА) {
        if (ГРЕШКА instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (ГРЕШКА instanceof java.lang.IllegalArgumentException) return new неважеће_аргумент_изузетак("인수의 값이나 범위를 확인하십시오.");
        if (ГРЕШКА instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (ГРЕШКА instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (ГРЕШКА instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (ГРЕШКА instanceof java.lang.NullPointerException) return new без_вредности_Литература_изузетак("비어 있는 참조입니다.");
        return new 실행예외(ГРЕШКА.getMessage());
    }
}
