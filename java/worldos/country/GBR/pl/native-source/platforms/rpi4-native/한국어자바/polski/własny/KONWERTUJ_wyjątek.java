// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;

/** 표준 Java 오류를 polski API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class KONWERTUJ_wyjątek {
    private KONWERTUJ_wyjątek() {}
    public static We_Wy_wyjątek We_Wy(java.io.IOException błąd) {
        if (błąd instanceof We_Wy_wyjątek) return (We_Wy_wyjątek)błąd;
        if (błąd instanceof java.net.SocketTimeoutException) return new chwileczkę_TIMEOUT_wyjątek("komunikacja 대기시간을 넘었습니다.");
        if (błąd instanceof java.net.UnknownHostException) return new ADRES_WYSZUKAJ_wyjątek("주소를 확인할 identyfikator 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (błąd instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 kolumna_WARTOŚĆ identyfikator 없습니다.");
        if (błąd instanceof java.net.SocketException) return new komunikacja_wyjątek("komunikacja Połącz 작업 awaria_WARTOŚĆ: " + błąd.getMessage());
        return new We_Wy_wyjątek("We_Wy 작업 awaria_WARTOŚĆ: " + błąd.getMessage());
    }
    public static RuntimeException Wykonaj_polecenie(RuntimeException błąd) {
        if (błąd instanceof java.lang.NumberFormatException) return new identyfikator_format_awaria("숫자의 형식이나 범위를 확인하십시오.");
        if (błąd instanceof java.lang.IllegalArgumentException) return new nieważny_argument_wyjątek("인수의 값이나 범위를 확인하십시오.");
        if (błąd instanceof java.lang.ArrayIndexOutOfBoundsException) return new granice_tablicy_wyjątek("배열의 범위를 벗어났습니다.");
        if (błąd instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (błąd instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (błąd instanceof java.lang.NullPointerException) return new pusta_referencja_wyjątek("비어 있는 참조입니다.");
        return new wykonanie_wyjątek(błąd.getMessage());
    }
}
