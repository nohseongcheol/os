// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;

/** 표준 Java 오류를 Català API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERT_excepció {
    private CONVERT_excepció() {}
    public static E_S_excepció E_S(java.io.IOException s_ha_produït_un_error) {
        if (s_ha_produït_un_error instanceof E_S_excepció) return (E_S_excepció)s_ha_produït_un_error;
        if (s_ha_produït_un_error instanceof java.net.SocketTimeoutException) return new Espera_TIMEOUT_excepció("통신 대기시간을 넘었습니다.");
        if (s_ha_produït_un_error instanceof java.net.UnknownHostException) return new ADREÇA_Cerca_excepció("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (s_ha_produït_un_error instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 COLUMNA_VALOR 수 없습니다.");
        if (s_ha_produït_un_error instanceof java.net.SocketException) return new 통신예외("통신 Connecta 작업 error_VALOR: " + s_ha_produït_un_error.getMessage());
        return new E_S_excepció("E_S 작업 error_VALOR: " + s_ha_produït_un_error.getMessage());
    }
    public static RuntimeException Executa_ordre(RuntimeException s_ha_produït_un_error) {
        if (s_ha_produït_un_error instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (s_ha_produït_un_error instanceof java.lang.IllegalArgumentException) return new invàlid_arg_excepció("인수의 값이나 범위를 확인하십시오.");
        if (s_ha_produït_un_error instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (s_ha_produït_un_error instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (s_ha_produït_un_error instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (s_ha_produït_un_error instanceof java.lang.NullPointerException) return new NUL_Referència_excepció("비어 있는 참조입니다.");
        return new 실행예외(s_ha_produït_un_error.getMessage());
    }
}
