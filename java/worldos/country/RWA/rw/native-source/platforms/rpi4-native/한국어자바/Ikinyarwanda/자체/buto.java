// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ikinyarwanda.자체;
/** 자체 화면에서 Igikorwa 알림을 보내는 buto. */
public final class buto extends 화면구성요소 {
    public buto(String Umwandiko, int 가로, int 세로, int 폭, int 높이, 동작받이 받이) {
        throw new 상태예외("자체 JVM의 Ikinyarwanda buto 생성 기능이 필요합니다.");
    }
    public native void 동작맡기기(동작받이 받이);
}
