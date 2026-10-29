// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 vindauge 관리 기능에 직접 연결되는 vindauge. */
public final class vindauge extends 화면구성요소 {
    public vindauge(String vindauge_Tittel, int 폭, int 높이) {
        throw new status_unntak("자체 JVM의 한국어 vindauge generere 기능이 필요합니다.");
    }
    public native void leggje_til_element(화면구성요소 element_VALUE);
    public native void vise_vindauge();
    public native void Lukk();
    public native boolean 보이는가();
}
