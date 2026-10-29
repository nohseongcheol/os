// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;

/** 표준 Java 오류를 Euskara API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class BIHURTU_salbuespen {
    private BIHURTU_salbuespen() {}
    public static S_I_salbuespen S_I(java.io.IOException errorea) {
        if (errorea instanceof S_I_salbuespen) return (S_I_salbuespen)errorea;
        if (errorea instanceof java.net.SocketTimeoutException) return new itxaron_DENBORA_MUGA_salbuespen("통신 대기시간을 넘었습니다.");
        if (errorea instanceof java.net.UnknownHostException) return new helbide_BEGIRATU_salbuespen("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (errorea instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 zutabe_balio 수 없습니다.");
        if (errorea instanceof java.net.SocketException) return new 통신예외("통신 Konektatu 작업 hutsegite_balio: " + errorea.getMessage());
        return new S_I_salbuespen("S_I 작업 hutsegite_balio: " + errorea.getMessage());
    }
    public static RuntimeException exekutatu_komando(RuntimeException errorea) {
        if (errorea instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (errorea instanceof java.lang.IllegalArgumentException) return new baliogabe_arg_salbuespen("인수의 값이나 범위를 확인하십시오.");
        if (errorea instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (errorea instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (errorea instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (errorea instanceof java.lang.NullPointerException) return new nulu_Erreferentzia_materiala_salbuespen("비어 있는 참조입니다.");
        return new 실행예외(errorea.getMessage());
    }
}
