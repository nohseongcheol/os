// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.своє;

/** 표준 Java 오류를 українська API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class перетворити_виняток {
    private перетворити_виняток() {}
    public static ввід_вивід_виняток ввід_вивід(java.io.IOException ПОМИЛКА) {
        if (ПОМИЛКА instanceof ввід_вивід_виняток) return (ввід_вивід_виняток)ПОМИЛКА;
        if (ПОМИЛКА instanceof java.net.SocketTimeoutException) return new 대기시간초과예외("통신 대기시간을 넘었습니다.");
        if (ПОМИЛКА instanceof java.net.UnknownHostException) return new адреса_Інформування_виняток("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (ПОМИЛКА instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 стовпець_значення 수 없습니다.");
        if (ПОМИЛКА instanceof java.net.SocketException) return new 통신예외("통신 З_єднання 작업 неполадка_значення: " + ПОМИЛКА.getMessage());
        return new ввід_вивід_виняток("ввід_вивід 작업 неполадка_значення: " + ПОМИЛКА.getMessage());
    }
    public static RuntimeException Виконати_команда(RuntimeException ПОМИЛКА) {
        if (ПОМИЛКА instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (ПОМИЛКА instanceof java.lang.IllegalArgumentException) return new недійсний_аргумент_виняток("인수의 값이나 범위를 확인하십시오.");
        if (ПОМИЛКА instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (ПОМИЛКА instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (ПОМИЛКА instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (ПОМИЛКА instanceof java.lang.NullPointerException) return new Null_значення_довідка_виняток("비어 있는 참조입니다.");
        return new 실행예외(ПОМИЛКА.getMessage());
    }
}
