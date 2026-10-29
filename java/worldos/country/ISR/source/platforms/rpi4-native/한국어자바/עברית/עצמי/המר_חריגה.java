// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;

/** 표준 Java 오류를 עברית API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class המר_חריגה {
    private המר_חריגה() {}
    public static קלט_פלט_חריגה קלט_פלט(java.io.IOException שגיאה) {
        if (שגיאה instanceof קלט_פלט_חריגה) return (קלט_פלט_חריגה)שגיאה;
        if (שגיאה instanceof java.net.SocketTimeoutException) return new רק_רגע_פסק_זמן_חריגה("통신 대기시간을 넘었습니다.");
        if (שגיאה instanceof java.net.UnknownHostException) return new למען_חפושׂ_חריגה("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (שגיאה instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 עמודה_ערך 수 없습니다.");
        if (שגיאה instanceof java.net.SocketException) return new 통신예외("통신 חיבור 작업 כשל_ערך: " + שגיאה.getMessage());
        return new קלט_פלט_חריגה("קלט_פלט 작업 כשל_ערך: " + שגיאה.getMessage());
    }
    public static RuntimeException לבצע_פקודה(RuntimeException שגיאה) {
        if (שגיאה instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (שגיאה instanceof java.lang.IllegalArgumentException) return new לא_חוקי_ארגומנט_חריגה("인수의 값이나 범위를 확인하십시오.");
        if (שגיאה instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (שגיאה instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (שגיאה instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (שגיאה instanceof java.lang.NullPointerException) return new הפניה_חסרת_אובייקט_חריגה("비어 있는 참조입니다.");
        return new 실행예외(שגיאה.getMessage());
    }
}
