// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;
/** savs 화면에서 Darbība 알림을 보내는 Pogas. */
public final class Pogas extends 화면구성요소 {
    public Pogas(String Teksts, int 가로, int vertikāle_amats, int 폭, int 높이, 동작받이 받이) {
        throw new Statuss_izņēmums("savs JVM의 Latviešu Pogas ģenerēt 기능이 필요합니다.");
    }
    public native void 동작맡기기(동작받이 받이);
}
