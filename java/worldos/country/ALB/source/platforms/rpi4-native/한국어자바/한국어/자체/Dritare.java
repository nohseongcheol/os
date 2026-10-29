// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 Dritare 관리 기능에 직접 연결되는 Dritare. */
public final class Dritare extends 화면구성요소 {
    public Dritare(String dritare_Titulli, int 폭, int 높이) {
        throw new status_përjashtim("자체 JVM의 한국어 Dritare gjeneroj 기능이 필요합니다.");
    }
    public native void shto_element(화면구성요소 element_VALUE);
    public native void shfaq_dritare();
    public native void Mbyll();
    public native boolean 보이는가();
}
