// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;
/** oma JVM과 커널의 aken 관리 기능에 직접 연결되는 aken. */
public final class aken extends 화면구성요소 {
    public aken(String aken_teos, int 폭, int 높이) {
        throw new Olek_erand("oma JVM의 Eesti aken genereerima 기능이 필요합니다.");
    }
    public native void Lisa_element(화면구성요소 element_VALUE);
    public native void saade_aken();
    public native void Suletud();
    public native boolean 보이는가();
}
