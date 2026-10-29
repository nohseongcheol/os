// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 화면에서 Handling 알림을 보내는 knapp. */
public final class knapp extends 화면구성요소 {
    public knapp(String Tekst, int 가로, int vertikalvising_plassere, int 폭, int 높이, 동작받이 받이) {
        throw new status_unntak("자체 JVM의 한국어 knapp generere 기능이 필요합니다.");
    }
    public native void 동작맡기기(동작받이 받이);
}
