// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;

/** 표준 Java 오류를 Íslenska API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERT_undantekning {
    private CONVERT_undantekning() {}
    public static I_Ú_undantekning I_Ú(java.io.IOException Villa) {
        if (Villa instanceof I_Ú_undantekning) return (I_Ú_undantekning)Villa;
        if (Villa instanceof java.net.SocketTimeoutException) return new Bíddu_TIMEOUT_undantekning("통신 대기시간을 넘었습니다.");
        if (Villa instanceof java.net.UnknownHostException) return new slóð_LOOKUP_undantekning("주소를 확인할 númer 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (Villa instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 COLUMN_VALUE númer 없습니다.");
        if (Villa instanceof java.net.SocketException) return new 통신예외("통신 Tengjast 작업 bilun_VALUE: " + Villa.getMessage());
        return new I_Ú_undantekning("I_Ú 작업 bilun_VALUE: " + Villa.getMessage());
    }
    public static RuntimeException keyra_skipun(RuntimeException Villa) {
        if (Villa instanceof java.lang.NumberFormatException) return new númer_snið_bilun("숫자의 형식이나 범위를 확인하십시오.");
        if (Villa instanceof java.lang.IllegalArgumentException) return new ógilt_frumbreyta_undantekning("인수의 값이나 범위를 확인하십시오.");
        if (Villa instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (Villa instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (Villa instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (Villa instanceof java.lang.NullPointerException) return new NULL_tilvísun_undantekning("비어 있는 참조입니다.");
        return new 실행예외(Villa.getMessage());
    }
}
