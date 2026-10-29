// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 화면에서 কাৰ্য্য 알림을 보내는 বুটাম. */
public final class বুটাম extends 화면구성요소 {
    public বুটাম(String টেক্সট, int 가로, int উলম্ব_স্থান_সলনি_কৰক, int 폭, int 높이, 동작받이 받이) {
        throw new 상태예외("자체 JVM의 한국어 বুটাম সৃষ্টি_কৰক 기능이 필요합니다.");
    }
    public native void 동작맡기기(동작받이 받이);
}
