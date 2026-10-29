// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 표준 Java 오류를 한국어 API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class 예외변환 {
    private 예외변환() {}
    public static ចូល_ចេញ_ការលើកលែង ចូល_ចេញ(java.io.IOException កំហុស) {
        if (កំហុស instanceof ចូល_ចេញ_ការលើកលែង) return (ចូល_ចេញ_ការលើកលែង)កំហុស;
        if (កំហុស instanceof java.net.SocketTimeoutException) return new រង់ចាំ_អស់ម៉ោង_ការលើកលែង("통신 대기시간을 넘었습니다.");
        if (កំហុស instanceof java.net.UnknownHostException) return new អ៊ីម៉ែល_រុករក_ការលើកលែង("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (កំហុស instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 ជួរឈរ_តំលៃ 수 없습니다.");
        if (កំហុស instanceof java.net.SocketException) return new 통신예외("통신 ភ្ជាប់ 작업 បរាជ័យ_តំលៃ: " + កំហុស.getMessage());
        return new ចូល_ចេញ_ការលើកលែង("ចូល_ចេញ 작업 បរាជ័យ_តំលៃ: " + កំហុស.getMessage());
    }
    public static RuntimeException អនុវត្ត_ពាក្យបញ្ជា(RuntimeException កំហុស) {
        if (កំហុស instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (កំហុស instanceof java.lang.IllegalArgumentException) return new មិនត្រឹមត្រូវ_អាគុយម៉ង់_ការលើកលែង("인수의 값이나 범위를 확인하십시오.");
        if (កំហុស instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (កំហុស instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (កំហុស instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (កំហុស instanceof java.lang.NullPointerException) return new ទទេ_យោង_ការលើកលែង("비어 있는 참조입니다.");
        return new 실행예외(កំហុស.getMessage());
    }
}
