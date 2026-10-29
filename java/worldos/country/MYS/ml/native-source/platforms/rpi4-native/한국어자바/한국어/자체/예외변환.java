// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 표준 Java 오류를 한국어 API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class 예외변환 {
    private 예외변환() {}
    public static ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(java.io.IOException പിശക്) {
        if (പിശക് instanceof ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ) return (ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ)പിശക്;
        if (പിശക് instanceof java.net.SocketTimeoutException) return new കാക്കുക_ടൈംഔട്ട്_ഒഴിവാക്കൽ("통신 대기시간을 넘었습니다.");
        if (പിശക് instanceof java.net.UnknownHostException) return new ഇമെയിൽ_തിരഞ്ഞു_നോക്കൽ_ഒഴിവാക്കൽ("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (പിശക് instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 നിര_മൂല്യം 수 없습니다.");
        if (പിശക് instanceof java.net.SocketException) return new 통신예외("통신 കണക്ടു്_ചെയ്യുക 작업 പരാജയം_മൂല്യം: " + പിശക്.getMessage());
        return new ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ("ഇന്_പുട്ട്_ഔട്ട്_പുട്ട് 작업 പരാജയം_മൂല്യം: " + പിശക്.getMessage());
    }
    public static RuntimeException നടപ്പാക്കുക_കമാന്_ഡ്(RuntimeException പിശക്) {
        if (പിശക് instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (പിശക് instanceof java.lang.IllegalArgumentException) return new അസാധുവായ_ആര്_ഗ്യുമെന്_റ്_ഒഴിവാക്കൽ("인수의 값이나 범위를 확인하십시오.");
        if (പിശക് instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (പിശക് instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (പിശക് instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (പിശക് instanceof java.lang.NullPointerException) return new അജ്ഞാത_പരാമര്_ശം_ഒഴിവാക്കൽ("비어 있는 참조입니다.");
        return new 실행예외(പിശക്.getMessage());
    }
}
