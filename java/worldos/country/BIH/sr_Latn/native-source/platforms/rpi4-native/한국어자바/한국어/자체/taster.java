// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 화면에서 radnja 알림을 보내는 taster. */
public final class taster extends 화면구성요소 {
    public taster(String SMS, int 가로, int vertikala_pozicija, int 폭, int 높이, 동작받이 받이) {
        throw new Status_izuzetak("자체 JVM의 한국어 taster generisati 기능이 필요합니다.");
    }
    public native void 동작맡기기(동작받이 받이);
}
