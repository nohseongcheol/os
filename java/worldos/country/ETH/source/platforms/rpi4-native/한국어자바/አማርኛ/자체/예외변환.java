// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;

/** 표준 Java 오류를 አማርኛ API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class 예외변환 {
    private 예외변환() {}
    public static ግቤት_ውጤት_ልዩነት ግቤት_ውጤት(java.io.IOException ስህተት) {
        if (ስህተት instanceof ግቤት_ውጤት_ልዩነት) return (ግቤት_ውጤት_ልዩነት)ስህተት;
        if (ስህተት instanceof java.net.SocketTimeoutException) return new 대기시간초과예외("통신 대기시간을 넘었습니다.");
        if (ስህተት instanceof java.net.UnknownHostException) return new አድራሻ_ፍለጋ_ልዩነት("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (ስህተት instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 አምድ_እሴት 수 없습니다.");
        if (ስህተት instanceof java.net.SocketException) return new 통신예외("통신 መገናኛ 작업 ተስኖት_እሴት: " + ስህተት.getMessage());
        return new ግቤት_ውጤት_ልዩነት("ግቤት_ውጤት 작업 ተስኖት_እሴት: " + ስህተት.getMessage());
    }
    public static RuntimeException ፈጽም_ትእዛዝ(RuntimeException ስህተት) {
        if (ስህተት instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (ስህተት instanceof java.lang.IllegalArgumentException) return new ልክ_ያልኾነ_ነጋሪ_እሴት_ልዩነት("인수의 값이나 범위를 확인하십시오.");
        if (ስህተት instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (ስህተት instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (ስህተት instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (ስህተት instanceof java.lang.NullPointerException) return new አልቦ_ማጣቀሻ_ልዩነት("비어 있는 참조입니다.");
        return new 실행예외(ስህተት.getMessage());
    }
}
