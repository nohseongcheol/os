// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자체;

/** 표준 Java 오류를 தமிழ் API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class 예외변환 {
    private 예외변환() {}
    public static உள்ளீடு_வெளியீடு_விதிவிலக்கு உள்ளீடு_வெளியீடு(java.io.IOException பிழை) {
        if (பிழை instanceof உள்ளீடு_வெளியீடு_விதிவிலக்கு) return (உள்ளீடு_வெளியீடு_விதிவிலக்கு)பிழை;
        if (பிழை instanceof java.net.SocketTimeoutException) return new 대기시간초과예외("통신 대기시간을 넘었습니다.");
        if (பிழை instanceof java.net.UnknownHostException) return new முகவரி_தேடுதல்_விதிவிலக்கு("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (பிழை instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 நெடுவரிசை_மதிப்பு 수 없습니다.");
        if (பிழை instanceof java.net.SocketException) return new 통신예외("통신 இணைக்க 작업 செயலிழப்பு_மதிப்பு: " + பிழை.getMessage());
        return new உள்ளீடு_வெளியீடு_விதிவிலக்கு("உள்ளீடு_வெளியீடு 작업 செயலிழப்பு_மதிப்பு: " + பிழை.getMessage());
    }
    public static RuntimeException இயக்கு_கட்டளை(RuntimeException பிழை) {
        if (பிழை instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (பிழை instanceof java.lang.IllegalArgumentException) return new செல்லுபடியாகாத_மதிப்புரு_விதிவிலக்கு("인수의 값이나 범위를 확인하십시오.");
        if (பிழை instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (பிழை instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (பிழை instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (பிழை instanceof java.lang.NullPointerException) return new வெற்றுக்_குறிப்பு_விதிவிலக்கு("비어 있는 참조입니다.");
        return new 실행예외(பிழை.getMessage());
    }
}
