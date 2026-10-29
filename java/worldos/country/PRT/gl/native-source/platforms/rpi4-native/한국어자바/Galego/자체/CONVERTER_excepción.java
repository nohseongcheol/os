// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;

/** 표준 Java 오류를 Galego API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERTER_excepción {
    private CONVERTER_excepción() {}
    public static E_S_excepción E_S(java.io.IOException ERRO) {
        if (ERRO instanceof E_S_excepción) return (E_S_excepción)ERRO;
        if (ERRO instanceof java.net.SocketTimeoutException) return new agarda_TIMEOUT_excepción("통신 대기시간을 넘었습니다.");
        if (ERRO instanceof java.net.UnknownHostException) return new ENDEREZO_Busca_excepción("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (ERRO instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 COLUMNA_VALOR 수 없습니다.");
        if (ERRO instanceof java.net.SocketException) return new 통신예외("통신 Conectar 작업 erro_VALOR: " + ERRO.getMessage());
        return new E_S_excepción("E_S 작업 erro_VALOR: " + ERRO.getMessage());
    }
    public static RuntimeException executar_comando(RuntimeException ERRO) {
        if (ERRO instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (ERRO instanceof java.lang.IllegalArgumentException) return new non_válido_argumento_excepción("인수의 값이나 범위를 확인하십시오.");
        if (ERRO instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (ERRO instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (ERRO instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (ERRO instanceof java.lang.NullPointerException) return new NULO_Material_de_referencia_excepción("비어 있는 참조입니다.");
        return new 실행예외(ERRO.getMessage());
    }
}
