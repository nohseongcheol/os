// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;

/** 표준 Java 오류를 Italiano API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERTI_eccezione {
    private CONVERTI_eccezione() {}
    public static I_O_eccezione I_O(java.io.IOException errore) {
        if (errore instanceof I_O_eccezione) return (I_O_eccezione)errore;
        if (errore instanceof java.net.SocketTimeoutException) return new aspetta_TIMEOUT_eccezione("comunicazione 대기시간을 넘었습니다.");
        if (errore instanceof java.net.UnknownHostException) return new e_mail_CERCA_eccezione("주소를 확인할 numero 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (errore instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 colonna_VALORE numero 없습니다.");
        if (errore instanceof java.net.SocketException) return new comunicazione_eccezione("comunicazione Connetti 작업 errore_VALORE: " + errore.getMessage());
        return new I_O_eccezione("I_O 작업 errore_VALORE: " + errore.getMessage());
    }
    public static RuntimeException Esegui_comando(RuntimeException errore) {
        if (errore instanceof java.lang.NumberFormatException) return new numero_formato_errore("숫자의 형식이나 범위를 확인하십시오.");
        if (errore instanceof java.lang.IllegalArgumentException) return new non_valida_argomento_eccezione("인수의 값이나 범위를 확인하십시오.");
        if (errore instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (errore instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (errore instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (errore instanceof java.lang.NullPointerException) return new riferimento_Null_eccezione("비어 있는 참조입니다.");
        return new esecuzione_eccezione(errore.getMessage());
    }
}
