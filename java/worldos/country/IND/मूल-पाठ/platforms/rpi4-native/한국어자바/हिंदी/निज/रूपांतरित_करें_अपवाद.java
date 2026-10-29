// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;

/** 표준 Java 오류를 हिंदी API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class रूपांतरित_करें_अपवाद {
    private रूपांतरित_करें_अपवाद() {}
    public static इनपुट_आउटपुट_अपवाद इनपुट_आउटपुट(java.io.IOException त्रुटि) {
        if (त्रुटि instanceof इनपुट_आउटपुट_अपवाद) return (इनपुट_आउटपुट_अपवाद)त्रुटि;
        if (त्रुटि instanceof java.net.SocketTimeoutException) return new 대기시간초과예외("통신 대기시간을 넘었습니다.");
        if (त्रुटि instanceof java.net.UnknownHostException) return new पता_लुकअप_अपवाद("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (त्रुटि instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 कालम_मान 수 없습니다.");
        if (त्रुटि instanceof java.net.SocketException) return new 통신예외("통신 जोड़ना 작업 विफलता_मान: " + त्रुटि.getMessage());
        return new इनपुट_आउटपुट_अपवाद("इनपुट_आउटपुट 작업 विफलता_मान: " + त्रुटि.getMessage());
    }
    public static RuntimeException निष्पादित_करें_आदेश(RuntimeException त्रुटि) {
        if (त्रुटि instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (त्रुटि instanceof java.lang.IllegalArgumentException) return new अमान्य_तर्क_अपवाद("인수의 값이나 범위를 확인하십시오.");
        if (त्रुटि instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (त्रुटि instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (त्रुटि instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (त्रुटि instanceof java.lang.NullPointerException) return new अकृत_उल्लेख_अपवाद("비어 있는 참조입니다.");
        return new 실행예외(त्रुटि.getMessage());
    }
}
