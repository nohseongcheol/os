// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;
/** 자체 JVM과 커널의 ffenestr 관리 기능에 직접 연결되는 ffenestr. */
public final class ffenestr extends 화면구성요소 {
    public ffenestr(String ffenestr_Teitl, int 폭, int 높이) {
        throw new cyflwr_eithriad("자체 JVM의 Cymraeg ffenestr cynhyrchu 기능이 필요합니다.");
    }
    public native void ychwanegu_elfen(화면구성요소 elfen_VALUE);
    public native void sioe_ffenestr();
    public native void Cau();
    public native boolean 보이는가();
}
