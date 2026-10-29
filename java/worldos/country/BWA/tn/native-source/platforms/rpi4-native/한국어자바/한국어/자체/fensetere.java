// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 fensetere 관리 기능에 직접 연결되는 fensetere. */
public final class fensetere extends 화면구성요소 {
    public fensetere(String fensetere_Setlhogo, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 fensetere 생성 기능이 필요합니다.");
    }
    public native void tsenya_tlhakakaelo(화면구성요소 tlhakakaelo_Boleng);
    public native void bontsha_fensetere();
    public native void tswala();
    public native boolean 보이는가();
}
