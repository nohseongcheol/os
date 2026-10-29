// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;

/** 표준 Java 오류를 magyar API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class konvertál_kivétel {
    private konvertál_kivétel() {}
    public static I_O_kivétel I_O(java.io.IOException HIBA) {
        if (HIBA instanceof I_O_kivétel) return (I_O_kivétel)HIBA;
        if (HIBA instanceof java.net.SocketTimeoutException) return new várj_IDŐTÚLLÉPÉS_kivétel("kommunikáció 대기시간을 넘었습니다.");
        if (HIBA instanceof java.net.UnknownHostException) return new CÍM_KERES_kivétel("주소를 확인할 szám 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (HIBA instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 OSZLOP_ÉRTÉK szám 없습니다.");
        if (HIBA instanceof java.net.SocketException) return new kommunikáció_kivétel("kommunikáció Kapcsolódás 작업 hiba_ÉRTÉK: " + HIBA.getMessage());
        return new I_O_kivétel("I_O 작업 hiba_ÉRTÉK: " + HIBA.getMessage());
    }
    public static RuntimeException végrehajt_parancs(RuntimeException HIBA) {
        if (HIBA instanceof java.lang.NumberFormatException) return new szám_formáz_hiba("숫자의 형식이나 범위를 확인하십시오.");
        if (HIBA instanceof java.lang.IllegalArgumentException) return new alaptalan_argumentum_kivétel("인수의 값이나 범위를 확인하십시오.");
        if (HIBA instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (HIBA instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (HIBA instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (HIBA instanceof java.lang.NullPointerException) return new null_hivatkozik_kivétel("비어 있는 참조입니다.");
        return new végrehajtás_kivétel(HIBA.getMessage());
    }
}
