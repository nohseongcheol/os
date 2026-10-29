// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 విండో 관리 기능에 직접 연결되는 విండో. */
public final class విండో extends 화면구성요소 {
    public విండో(String గవాక్షం_శీర్షిక, int 폭, int 높이) {
        throw new స్థితి_మినహాయింపు("자체 JVM의 한국어 విండో రూపొందించు 기능이 필요합니다.");
    }
    public native void జోడించు_మూలకం(화면구성요소 మూలకం_మూల్యం);
    public native void చూపించు_గవాక్షం();
    public native void మూసివేయి();
    public native boolean 보이는가();
}
