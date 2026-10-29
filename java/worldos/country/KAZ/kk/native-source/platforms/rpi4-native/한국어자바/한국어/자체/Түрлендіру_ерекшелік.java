// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 표준 Java 오류를 한국어 API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class Түрлендіру_ерекшелік {
    private Түрлендіру_ерекшелік() {}
    public static енгізу_шығару_ерекшелік енгізу_шығару(java.io.IOException Қате) {
        if (Қате instanceof енгізу_шығару_ерекшелік) return (енгізу_шығару_ерекшелік)Қате;
        if (Қате instanceof java.net.SocketTimeoutException) return new күте_тұрыңыз_ТАЙМ_АУТ_ерекшелік("통신 대기시간을 넘었습니다.");
        if (Қате instanceof java.net.UnknownHostException) return new мекенжай_Іздеу_ерекшелік("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (Қате instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 баған_мән 수 없습니다.");
        if (Қате instanceof java.net.SocketException) return new 통신예외("통신 Байланысу 작업 қате_мән: " + Қате.getMessage());
        return new енгізу_шығару_ерекшелік("енгізу_шығару 작업 қате_мән: " + Қате.getMessage());
    }
    public static RuntimeException орындау_пәрмен(RuntimeException Қате) {
        if (Қате instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (Қате instanceof java.lang.IllegalArgumentException) return new дұрыс_емес_аргумент_ерекшелік("인수의 값이나 범위를 확인하십시오.");
        if (Қате instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (Қате instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (Қате instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (Қате instanceof java.lang.NullPointerException) return new бос_мән_Анықтамалық_ерекшелік("비어 있는 참조입니다.");
        return new 실행예외(Қате.getMessage());
    }
}
