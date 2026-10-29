// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 Fënster 관리 기능에 직접 연결되는 Fënster. */
public final class Fënster extends 화면구성요소 {
    public Fënster(String Fënster_Titel, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 Fënster generéieren 기능이 필요합니다.");
    }
    public native void derbäisetzen_Element(화면구성요소 Element_VALUE);
    public native void Show_Fënster();
    public native void Clôture();
    public native boolean 보이는가();
}
