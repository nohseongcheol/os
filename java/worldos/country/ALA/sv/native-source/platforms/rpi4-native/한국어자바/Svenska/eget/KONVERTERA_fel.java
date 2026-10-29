// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;

/** 표준 Java 오류를 Svenska API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class KONVERTERA_fel {
    private KONVERTERA_fel() {}
    public static indata_utleverans_fel indata_utleverans(java.io.IOException fel) {
        if (fel instanceof indata_utleverans_fel) return (indata_utleverans_fel)fel;
        if (fel instanceof java.net.SocketTimeoutException) return new vänta_TIMEOUT_fel("kommunikation 대기시간을 넘었습니다.");
        if (fel instanceof java.net.UnknownHostException) return new ADRESS_LETAUPP_fel("주소를 확인할 nummer 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (fel instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 spalt_värde nummer 없습니다.");
        if (fel instanceof java.net.SocketException) return new kommunikation_fel("kommunikation Anslut 작업 fel_värde: " + fel.getMessage());
        return new indata_utleverans_fel("indata_utleverans 작업 fel_värde: " + fel.getMessage());
    }
    public static RuntimeException köra_kommando(RuntimeException fel) {
        if (fel instanceof java.lang.NumberFormatException) return new nummer_format_fel("숫자의 형식이나 범위를 확인하십시오.");
        if (fel instanceof java.lang.IllegalArgumentException) return new ogiltig_argument_fel("인수의 값이나 범위를 확인하십시오.");
        if (fel instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (fel instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (fel instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (fel instanceof java.lang.NullPointerException) return new null_referens_fel("비어 있는 참조입니다.");
        return new körning_fel(fel.getMessage());
    }
}
