// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 화면에서 Aksie 알림을 보내는 knoppie. */
public final class knoppie extends 화면구성요소 {
    public knoppie(String Teks, int 가로, int Vertikaal_plaas, int 폭, int 높이, 동작받이 받이) {
        throw new stand_uitsondering("자체 JVM의 한국어 knoppie genereer 기능이 필요합니다.");
    }
    public native void 동작맡기기(동작받이 받이);
}
