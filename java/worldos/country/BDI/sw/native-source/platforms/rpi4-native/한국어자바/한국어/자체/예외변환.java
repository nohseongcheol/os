// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 표준 Java 오류를 한국어 API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class 예외변환 {
    private 예외변환() {}
    public static I_T_vighairi I_T(java.io.IOException kosa) {
        if (kosa instanceof I_T_vighairi) return (I_T_vighairi)kosa;
        if (kosa instanceof java.net.SocketTimeoutException) return new 대기시간초과예외("통신 대기시간을 넘었습니다.");
        if (kosa instanceof java.net.UnknownHostException) return new 주소확인예외("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (kosa instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 safuwima_thamani 수 없습니다.");
        if (kosa instanceof java.net.SocketException) return new 통신예외("통신 UNGANISHA 작업 kushindwa_thamani: " + kosa.getMessage());
        return new I_T_vighairi("I_T 작업 kushindwa_thamani: " + kosa.getMessage());
    }
    public static RuntimeException tekeleza_amri(RuntimeException kosa) {
        if (kosa instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (kosa instanceof java.lang.IllegalArgumentException) return new batili_hoja_vighairi("인수의 값이나 범위를 확인하십시오.");
        if (kosa instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (kosa instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (kosa instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (kosa instanceof java.lang.NullPointerException) return new batili_Marejeleo_vighairi("비어 있는 참조입니다.");
        return new 실행예외(kosa.getMessage());
    }
}
