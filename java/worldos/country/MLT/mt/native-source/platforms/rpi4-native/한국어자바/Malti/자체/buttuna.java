// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malti.자체;
/** 자체 화면에서 azzjoni 알림을 보내는 buttuna. */
public final class buttuna extends 화면구성요소 {
    public buttuna(String SMS, int 가로, int Vertikali_pożizzjoni, int 폭, int 높이, 동작받이 받이) {
        throw new 상태예외("자체 JVM의 Malti buttuna iġġenera 기능이 필요합니다.");
    }
    public native void 동작맡기기(동작받이 받이);
}
