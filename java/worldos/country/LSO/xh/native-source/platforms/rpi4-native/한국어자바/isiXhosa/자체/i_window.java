// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package isiXhosa.자체;
/** 자체 JVM과 커널의 i_window 관리 기능에 직접 연결되는 i_window. */
public final class i_window extends 화면구성요소 {
    public i_window(String i_window_Isihloko, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 isiXhosa i_window 생성 기능이 필요합니다.");
    }
    public native void yongeza_ielement(화면구성요소 ielement_ixabiso);
    public native void bonisa_i_window();
    public native void Vala();
    public native boolean 보이는가();
}
