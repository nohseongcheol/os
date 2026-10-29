// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 표준 Java 오류를 한국어 API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERT_uitsondering {
    private CONVERT_uitsondering() {}
    public static I_O_uitsondering I_O(java.io.IOException Fout) {
        if (Fout instanceof I_O_uitsondering) return (I_O_uitsondering)Fout;
        if (Fout instanceof java.net.SocketTimeoutException) return new wag_UITTELLING_uitsondering("통신 대기시간을 넘었습니다.");
        if (Fout instanceof java.net.UnknownHostException) return new adres_LOOKUP_uitsondering("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (Fout instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 kolom_VALUE 수 없습니다.");
        if (Fout instanceof java.net.SocketException) return new 통신예외("통신 Koppel 작업 faling_VALUE: " + Fout.getMessage());
        return new I_O_uitsondering("I_O 작업 faling_VALUE: " + Fout.getMessage());
    }
    public static RuntimeException uitvoer_bevel(RuntimeException Fout) {
        if (Fout instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (Fout instanceof java.lang.IllegalArgumentException) return new ongeldig_argument_uitsondering("인수의 값이나 범위를 확인하십시오.");
        if (Fout instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (Fout instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (Fout instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (Fout instanceof java.lang.NullPointerException) return new nul_Naslaan_uitsondering("비어 있는 참조입니다.");
        return new 실행예외(Fout.getMessage());
    }
}
