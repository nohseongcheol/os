// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 विंडो 관리 기능에 직접 연결되는 विंडो. */
public final class विंडो extends 화면구성요소 {
    public विंडो(String विंडो_शीर्षक, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 विंडो तयार_करचें 기능이 필요합니다.");
    }
    public native void संयोजन_करचें_मूलतत्व(화면구성요소 मूलतत्व_मोल);
    public native void शो_विंडो();
    public native void शेवट();
    public native boolean 보이는가();
}
