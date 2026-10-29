// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 표준 Java 오류를 한국어 API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERT_istisno {
    private CONVERT_istisno() {}
    public static I_O_istisno I_O(java.io.IOException Xato) {
        if (Xato instanceof I_O_istisno) return (I_O_istisno)Xato;
        if (Xato instanceof java.net.SocketTimeoutException) return new bir_daqiqa_TANAFFUS_istisno("통신 대기시간을 넘었습니다.");
        if (Xato instanceof java.net.UnknownHostException) return new manzil_LOOKUP_istisno("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (Xato instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 ustun_VALUE 수 없습니다.");
        if (Xato instanceof java.net.SocketException) return new 통신예외("통신 Ulanish 작업 to_xtab_qolish_VALUE: " + Xato.getMessage());
        return new I_O_istisno("I_O 작업 to_xtab_qolish_VALUE: " + Xato.getMessage());
    }
    public static RuntimeException bajarmoq_buyruq(RuntimeException Xato) {
        if (Xato instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (Xato instanceof java.lang.IllegalArgumentException) return new xato_dalil_istisno("인수의 값이나 범위를 확인하십시오.");
        if (Xato instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (Xato instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (Xato instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (Xato instanceof java.lang.NullPointerException) return new nul_Ma_lumotnomalar_istisno("비어 있는 참조입니다.");
        return new 실행예외(Xato.getMessage());
    }
}
