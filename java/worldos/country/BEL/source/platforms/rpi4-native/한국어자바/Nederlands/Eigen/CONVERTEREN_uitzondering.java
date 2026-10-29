// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;

/** 표준 Java 오류를 Nederlands API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERTEREN_uitzondering {
    private CONVERTEREN_uitzondering() {}
    public static I_O_uitzondering I_O(java.io.IOException fout) {
        if (fout instanceof I_O_uitzondering) return (I_O_uitzondering)fout;
        if (fout instanceof java.net.SocketTimeoutException) return new wachten_TIMEOUT_uitzondering("communicatie 대기시간을 넘었습니다.");
        if (fout instanceof java.net.UnknownHostException) return new ADRES_ZOEKEN_uitzondering("주소를 확인할 nummer 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (fout instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 KOLOM_WAARDE nummer 없습니다.");
        if (fout instanceof java.net.SocketException) return new communicatie_uitzondering("communicatie Verbinden 작업 fout_WAARDE: " + fout.getMessage());
        return new I_O_uitzondering("I_O 작업 fout_WAARDE: " + fout.getMessage());
    }
    public static RuntimeException Uitvoeren_opdracht(RuntimeException fout) {
        if (fout instanceof java.lang.NumberFormatException) return new nummer_opmaak_fout("숫자의 형식이나 범위를 확인하십시오.");
        if (fout instanceof java.lang.IllegalArgumentException) return new nietig_argument_uitzondering("인수의 값이나 범위를 확인하십시오.");
        if (fout instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (fout instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (fout instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (fout instanceof java.lang.NullPointerException) return new LEEG_verwijzen_uitzondering("비어 있는 참조입니다.");
        return new uitvoerbewerking_uitzondering(fout.getMessage());
    }
}
