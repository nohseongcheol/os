// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;

/** 표준 Java 오류를 Português API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERTER_exceção {
    private CONVERTER_exceção() {}
    public static E_S_exceção E_S(java.io.IOException erro) {
        if (erro instanceof E_S_exceção) return (E_S_exceção)erro;
        if (erro instanceof java.net.SocketTimeoutException) return new aguarde_TEMPOLIMITE_exceção("comunicação 대기시간을 넘었습니다.");
        if (erro instanceof java.net.UnknownHostException) return new email_PROC_exceção("주소를 확인할 número 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (erro instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 COL_VALOR número 없습니다.");
        if (erro instanceof java.net.SocketException) return new comunicação_exceção("comunicação Ligar 작업 falha_VALOR: " + erro.getMessage());
        return new E_S_exceção("E_S 작업 falha_VALOR: " + erro.getMessage());
    }
    public static RuntimeException Executar_comando(RuntimeException erro) {
        if (erro instanceof java.lang.NumberFormatException) return new número_formato_falha("숫자의 형식이나 범위를 확인하십시오.");
        if (erro instanceof java.lang.IllegalArgumentException) return new inválido_argumento_exceção("인수의 값이나 범위를 확인하십시오.");
        if (erro instanceof java.lang.ArrayIndexOutOfBoundsException) return new limites_da_matriz_exceção("배열의 범위를 벗어났습니다.");
        if (erro instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (erro instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (erro instanceof java.lang.NullPointerException) return new referência_nula_exceção("비어 있는 참조입니다.");
        return new execução_exceção(erro.getMessage());
    }
}
