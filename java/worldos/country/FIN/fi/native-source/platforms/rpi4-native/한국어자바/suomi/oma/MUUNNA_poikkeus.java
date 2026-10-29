// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;

/** 표준 Java 오류를 suomi API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class MUUNNA_poikkeus {
    private MUUNNA_poikkeus() {}
    public static I_O_poikkeus I_O(java.io.IOException VIRHE) {
        if (VIRHE instanceof I_O_poikkeus) return (I_O_poikkeus)VIRHE;
        if (VIRHE instanceof java.net.SocketTimeoutException) return new odottaa_AIKAKATKAISU_poikkeus("통신 대기시간을 넘었습니다.");
        if (VIRHE instanceof java.net.UnknownHostException) return new OSOITE_HAKU_poikkeus("주소를 확인할 numero 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (VIRHE instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 SARAKE_ARVO numero 없습니다.");
        if (VIRHE instanceof java.net.SocketException) return new 통신예외("통신 Yhdistä 작업 virhe_ARVO: " + VIRHE.getMessage());
        return new I_O_poikkeus("I_O 작업 virhe_ARVO: " + VIRHE.getMessage());
    }
    public static RuntimeException Suorita_komento(RuntimeException VIRHE) {
        if (VIRHE instanceof java.lang.NumberFormatException) return new numero_muoto_virhe("숫자의 형식이나 범위를 확인하십시오.");
        if (VIRHE instanceof java.lang.IllegalArgumentException) return new pätemätön_argumentti_poikkeus("인수의 값이나 범위를 확인하십시오.");
        if (VIRHE instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (VIRHE instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (VIRHE instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (VIRHE instanceof java.lang.NullPointerException) return new TYHJÄ_viite_poikkeus("비어 있는 참조입니다.");
        return new suoritus_poikkeus(VIRHE.getMessage());
    }
}
