// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;

/** 표준 Java 오류를 Cymraeg API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERT_eithriad {
    private CONVERT_eithriad() {}
    public static I_O_eithriad I_O(java.io.IOException Gwall) {
        if (Gwall instanceof I_O_eithriad) return (I_O_eithriad)Gwall;
        if (Gwall instanceof java.net.SocketTimeoutException) return new aros_TIMEOUT_eithriad("통신 대기시간을 넘었습니다.");
        if (Gwall instanceof java.net.UnknownHostException) return new ADDRESS_LOOKUP_eithriad("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (Gwall instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 COLUMN_VALUE 수 없습니다.");
        if (Gwall instanceof java.net.SocketException) return new 통신예외("통신 Cysylltu 작업 methiant_VALUE: " + Gwall.getMessage());
        return new I_O_eithriad("I_O 작업 methiant_VALUE: " + Gwall.getMessage());
    }
    public static RuntimeException Gweithredu_gorchymyn(RuntimeException Gwall) {
        if (Gwall instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (Gwall instanceof java.lang.IllegalArgumentException) return new annilys_arg_eithriad("인수의 값이나 범위를 확인하십시오.");
        if (Gwall instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (Gwall instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (Gwall instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (Gwall instanceof java.lang.NullPointerException) return new NWL_cyfeiriad_eithriad("비어 있는 참조입니다.");
        return new 실행예외(Gwall.getMessage());
    }
}
