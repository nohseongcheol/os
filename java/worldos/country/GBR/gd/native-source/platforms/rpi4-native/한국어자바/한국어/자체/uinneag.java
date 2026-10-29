// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 uinneag 관리 기능에 직접 연결되는 uinneag. */
public final class uinneag extends 화면구성요소 {
    public uinneag(String uinneag_tiotal, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 uinneag gin 기능이 필요합니다.");
    }
    public native void cuir_ris_eileamaid(화면구성요소 eileamaid_VALUE);
    public native void show_uinneag();
    public native void dùin();
    public native boolean 보이는가();
}
