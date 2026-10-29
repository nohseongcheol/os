// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 화면에서 Veprim 알림을 보내는 Buton. */
public final class Buton extends 화면구성요소 {
    public Buton(String Teksti, int 가로, int Vertikal_pozicioni, int 폭, int 높이, 동작받이 받이) {
        throw new status_përjashtim("자체 JVM의 한국어 Buton gjeneroj 기능이 필요합니다.");
    }
    public native void 동작맡기기(동작받이 받이);
}
