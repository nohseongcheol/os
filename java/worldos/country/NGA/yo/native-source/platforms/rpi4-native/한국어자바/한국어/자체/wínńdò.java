// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 wínńdò 관리 기능에 직접 연결되는 wínńdò. */
public final class wínńdò extends 화면구성요소 {
    public wínńdò(String wínńdò_Àkọlé, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 wínńdò 생성 기능이 필요합니다.");
    }
    public native void ròmọ́_ìdá_ìpìlẹ̀(화면구성요소 ìdá_ìpìlẹ̀_iye);
    public native void ṣàfihàn_wínńdò();
    public native void Ti();
    public native boolean 보이는가();
}
