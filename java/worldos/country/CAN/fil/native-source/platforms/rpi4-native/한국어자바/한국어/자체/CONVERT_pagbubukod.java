// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 표준 Java 오류를 한국어 API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERT_pagbubukod {
    private CONVERT_pagbubukod() {}
    public static I_O_pagbubukod I_O(java.io.IOException error) {
        if (error instanceof I_O_pagbubukod) return (I_O_pagbubukod)error;
        if (error instanceof java.net.SocketTimeoutException) return new maghintay_TIMEOUT_pagbubukod("통신 대기시간을 넘었습니다.");
        if (error instanceof java.net.UnknownHostException) return new email_LOOKUP_pagbubukod("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (error instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 kolum_VALUE 수 없습니다.");
        if (error instanceof java.net.SocketException) return new 통신예외("통신 CONNECT 작업 pagpalya_VALUE: " + error.getMessage());
        return new I_O_pagbubukod("I_O 작업 pagpalya_VALUE: " + error.getMessage());
    }
    public static RuntimeException Mag_execute_utos(RuntimeException error) {
        if (error instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (error instanceof java.lang.IllegalArgumentException) return new hindi_tama_argumento_pagbubukod("인수의 값이나 범위를 확인하십시오.");
        if (error instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (error instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (error instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (error instanceof java.lang.NullPointerException) return new NULL_Sanggunian_pagbubukod("비어 있는 참조입니다.");
        return new 실행예외(error.getMessage());
    }
}
