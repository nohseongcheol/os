// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자체;

/** 표준 Java 오류를 ಕನ್ನಡ API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class 예외변환 {
    private 예외변환() {}
    public static ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್(java.io.IOException ದೋಷ) {
        if (ದೋಷ instanceof ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ) return (ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ)ದೋಷ;
        if (ದೋಷ instanceof java.net.SocketTimeoutException) return new 대기시간초과예외("통신 대기시간을 넘었습니다.");
        if (ದೋಷ instanceof java.net.UnknownHostException) return new ಇಮೇಲ್_ನೋಡುವ_ವಿನಾಯಿತಿ("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (ದೋಷ instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 ಲಂಬಸಾಲು_ಮೌಲ್ಯ 수 없습니다.");
        if (ದೋಷ instanceof java.net.SocketException) return new 통신예외("통신 ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು 작업 ವೈಫಲ್ಯ_ಮೌಲ್ಯ: " + ದೋಷ.getMessage());
        return new ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್_ವಿನಾಯಿತಿ("ಇನ್_ಪುಟ್_ಔಟ್_ಪುಟ್ 작업 ವೈಫಲ್ಯ_ಮೌಲ್ಯ: " + ದೋಷ.getMessage());
    }
    public static RuntimeException ಪೂರೈಸು_ಆದೇಶ(RuntimeException ದೋಷ) {
        if (ದೋಷ instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (ದೋಷ instanceof java.lang.IllegalArgumentException) return new ಅಮಾನ್ಯ_ವಾದ_ವಿನಾಯಿತಿ("인수의 값이나 범위를 확인하십시오.");
        if (ದೋಷ instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (ದೋಷ instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (ದೋಷ instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (ದೋಷ instanceof java.lang.NullPointerException) return new ಅಗೋಚರಿತ_ಉಲ್ಲೇಖ_ವಿನಾಯಿತಿ("비어 있는 참조입니다.");
        return new 실행예외(ದೋಷ.getMessage());
    }
}
