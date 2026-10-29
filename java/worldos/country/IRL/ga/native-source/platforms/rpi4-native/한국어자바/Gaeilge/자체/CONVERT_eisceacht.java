// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자체;

/** 표준 Java 오류를 Gaeilge API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERT_eisceacht {
    private CONVERT_eisceacht() {}
    public static I_O_eisceacht I_O(java.io.IOException ERREÁID) {
        if (ERREÁID instanceof I_O_eisceacht) return (I_O_eisceacht)ERREÁID;
        if (ERREÁID instanceof java.net.SocketTimeoutException) return new 대기시간초과예외("통신 대기시간을 넘었습니다.");
        if (ERREÁID instanceof java.net.UnknownHostException) return new ADDRESS_LOOKUP_eisceacht("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (ERREÁID instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 colún_VALUE 수 없습니다.");
        if (ERREÁID instanceof java.net.SocketException) return new 통신예외("통신 Nasc 작업 teip_VALUE: " + ERREÁID.getMessage());
        return new I_O_eisceacht("I_O 작업 teip_VALUE: " + ERREÁID.getMessage());
    }
    public static RuntimeException Rith_ordú(RuntimeException ERREÁID) {
        if (ERREÁID instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (ERREÁID instanceof java.lang.IllegalArgumentException) return new neamhbhailí_argóint_eisceacht("인수의 값이나 범위를 확인하십시오.");
        if (ERREÁID instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (ERREÁID instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (ERREÁID instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (ERREÁID instanceof java.lang.NullPointerException) return new NULL_Leabhair_thagartha_eisceacht("비어 있는 참조입니다.");
        return new 실행예외(ERREÁID.getMessage());
    }
}
