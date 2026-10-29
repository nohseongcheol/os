// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;

/** 표준 Java 오류를 čeština API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERT_výjimka {
    private CONVERT_výjimka() {}
    public static vstup_a_výstup_výjimka vstup_a_výstup(java.io.IOException chyba) {
        if (chyba instanceof vstup_a_výstup_výjimka) return (vstup_a_výstup_výjimka)chyba;
        if (chyba instanceof java.net.SocketTimeoutException) return new počkej_TIMEOUT_výjimka("komunikace 대기시간을 넘었습니다.");
        if (chyba instanceof java.net.UnknownHostException) return new ODKAZ_VYHLEDAT_výjimka("주소를 확인할 číslo 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (chyba instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 SLOUPEC_HODNOTA číslo 없습니다.");
        if (chyba instanceof java.net.SocketException) return new komunikace_výjimka("komunikace Připojit 작업 selhání_HODNOTA: " + chyba.getMessage());
        return new vstup_a_výstup_výjimka("vstup_a_výstup 작업 selhání_HODNOTA: " + chyba.getMessage());
    }
    public static RuntimeException Provést_příkaz(RuntimeException chyba) {
        if (chyba instanceof java.lang.NumberFormatException) return new číslo_formát_selhání("숫자의 형식이나 범위를 확인하십시오.");
        if (chyba instanceof java.lang.IllegalArgumentException) return new neplatný_argument_výjimka("인수의 값이나 범위를 확인하십시오.");
        if (chyba instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (chyba instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (chyba instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (chyba instanceof java.lang.NullPointerException) return new nulový_odkaz_výjimka("비어 있는 참조입니다.");
        return new spuštění_výjimka(chyba.getMessage());
    }
}
