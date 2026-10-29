// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;

/** 표준 Java 오류를 اردو API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class 예외변환 {
    private 예외변환() {}
    public static ان_پٹ_آؤٹ_پٹ_استثنا ان_پٹ_آؤٹ_پٹ(java.io.IOException غلطی) {
        if (غلطی instanceof ان_پٹ_آؤٹ_پٹ_استثنا) return (ان_پٹ_آؤٹ_پٹ_استثنا)غلطی;
        if (غلطی instanceof java.net.SocketTimeoutException) return new انتظار_ٹائم_آؤٹ_استثنا("통신 대기시간을 넘었습니다.");
        if (غلطی instanceof java.net.UnknownHostException) return new پتہ_لُک_اپ_استثنا("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (غلطی instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 کالم_قدر 수 없습니다.");
        if (غلطی instanceof java.net.SocketException) return new 통신예외("통신 متصل_ہوں 작업 ناکامی_قدر: " + غلطی.getMessage());
        return new ان_پٹ_آؤٹ_پٹ_استثنا("ان_پٹ_آؤٹ_پٹ 작업 ناکامی_قدر: " + غلطی.getMessage());
    }
    public static RuntimeException نفاذ_کریں_حکم(RuntimeException غلطی) {
        if (غلطی instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (غلطی instanceof java.lang.IllegalArgumentException) return new بے_جواز_دلائل_استثنا("인수의 값이나 범위를 확인하십시오.");
        if (غلطی instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (غلطی instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (غلطی instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (غلطی instanceof java.lang.NullPointerException) return new خالی_حوالہ_جات_استثنا("비어 있는 참조입니다.");
        return new 실행예외(غلطی.getMessage());
    }
}
