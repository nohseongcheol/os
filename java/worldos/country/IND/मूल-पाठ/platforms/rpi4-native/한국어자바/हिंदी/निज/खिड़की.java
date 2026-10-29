// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;
/** निज JVM과 커널의 खिड़की 관리 기능에 직접 연결되는 खिड़की. */
public final class खिड़की extends 화면구성요소 {
    public खिड़की(String विंडो_शीर्षक, int 폭, int 높이) {
        throw new अवस्था_अपवाद("निज JVM의 हिंदी खिड़की जनरेट_करें 기능이 필요합니다.");
    }
    public native void जोड़ें_तत्व(화면구성요소 तत्व_मान);
    public native void शो_विंडो();
    public native void बंदकरें();
    public native boolean 보이는가();
}
