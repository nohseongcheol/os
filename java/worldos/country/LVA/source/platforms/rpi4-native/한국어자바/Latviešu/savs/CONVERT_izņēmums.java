// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;

/** 표준 Java 오류를 Latviešu API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERT_izņēmums {
    private CONVERT_izņēmums() {}
    public static ievadizvade_izņēmums ievadizvade(java.io.IOException Kļūda) {
        if (Kļūda instanceof ievadizvade_izņēmums) return (ievadizvade_izņēmums)Kļūda;
        if (Kļūda instanceof java.net.SocketTimeoutException) return new pagaidi_NOILGUMS_izņēmums("통신 대기시간을 넘었습니다.");
        if (Kļūda instanceof java.net.UnknownHostException) return new adrese_LOOKUP_izņēmums("주소를 확인할 numurs 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (Kļūda instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 COLUMN_VALUE numurs 없습니다.");
        if (Kļūda instanceof java.net.SocketException) return new 통신예외("통신 Savienoties 작업 kļūme_VALUE: " + Kļūda.getMessage());
        return new ievadizvade_izņēmums("ievadizvade 작업 kļūme_VALUE: " + Kļūda.getMessage());
    }
    public static RuntimeException Izpildīt_komanda(RuntimeException Kļūda) {
        if (Kļūda instanceof java.lang.NumberFormatException) return new numurs_formāts_kļūme("숫자의 형식이나 범위를 확인하십시오.");
        if (Kļūda instanceof java.lang.IllegalArgumentException) return new nederīgs_arg_izņēmums("인수의 값이나 범위를 확인하십시오.");
        if (Kļūda instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (Kļūda instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (Kļūda instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (Kļūda instanceof java.lang.NullPointerException) return new NULL_Uzziņas_izņēmums("비어 있는 참조입니다.");
        return new 실행예외(Kļūda.getMessage());
    }
}
