// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 표준 Java 오류를 한국어 API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class 예외변환 {
    private 예외변환() {}
    public static ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ ଇନପୁଟ୍_ଆଉଟପୁଟ୍(java.io.IOException ତ୍ରୁଟି) {
        if (ତ୍ରୁଟି instanceof ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ) return (ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ)ତ୍ରୁଟି;
        if (ତ୍ରୁଟି instanceof java.net.SocketTimeoutException) return new 대기시간초과예외("통신 대기시간을 넘었습니다.");
        if (ତ୍ରୁଟି instanceof java.net.UnknownHostException) return new ଠିକଣା_ଦୃଷ୍ଟିପାତ_ବ୍ୟତିକ୍ରମ("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (ତ୍ରୁଟି instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 ସ୍ତମ୍ଭ_ମୂଲ୍ୟ 수 없습니다.");
        if (ତ୍ରୁଟି instanceof java.net.SocketException) return new 통신예외("통신 ସଂଯୋଗ_କରନ୍ତୁ 작업 ବିଫଳତା_ମୂଲ୍ୟ: " + ତ୍ରୁଟି.getMessage());
        return new ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ("ଇନପୁଟ୍_ଆଉଟପୁଟ୍ 작업 ବିଫଳତା_ମୂଲ୍ୟ: " + ତ୍ରୁଟି.getMessage());
    }
    public static RuntimeException ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(RuntimeException ତ୍ରୁଟି) {
        if (ତ୍ରୁଟି instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (ତ୍ରୁଟି instanceof java.lang.IllegalArgumentException) return new ଅବୈଧ_ଯୁକ୍ତି_ବ୍ୟତିକ୍ରମ("인수의 값이나 범위를 확인하십시오.");
        if (ତ୍ରୁଟି instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (ତ୍ରୁଟି instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (ତ୍ରୁଟି instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (ତ୍ରୁଟି instanceof java.lang.NullPointerException) return new ନିଷ୍ଫଳ_ପ୍ରସଙ୍ଗ_ବ୍ୟତିକ୍ରମ("비어 있는 참조입니다.");
        return new 실행예외(ତ୍ରୁଟି.getMessage());
    }
}
