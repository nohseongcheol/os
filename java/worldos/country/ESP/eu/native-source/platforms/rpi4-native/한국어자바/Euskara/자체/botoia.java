// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;
/** 자체 화면에서 Ekintza 알림을 보내는 botoia. */
public final class botoia extends 화면구성요소 {
    public botoia(String Testua, int 가로, int Bertikala_kargu, int 폭, int 높이, 동작받이 받이) {
        throw new Egoera_salbuespen("자체 JVM의 Euskara botoia sortu 기능이 필요합니다.");
    }
    public native void 동작맡기기(동작받이 받이);
}
