// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malti.자체;
/** 자체 JVM과 커널의 tieqa 관리 기능에 직접 연결되는 tieqa. */
public final class tieqa extends 화면구성요소 {
    public tieqa(String tieqa_Titlu, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 Malti tieqa iġġenera 기능이 필요합니다.");
    }
    public native void żied_element(화면구성요소 element_VALUE);
    public native void wera_tieqa();
    public native void agħlaq();
    public native boolean 보이는가();
}
