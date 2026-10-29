// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;
/** saját 화면에서 Művelet 알림을 보내는 gomb. */
public final class gomb extends 화면구성요소 {
    public gomb(String Szöveg, int 가로, int szektor_pozíció, int 폭, int 높이, 동작받이 받이) {
        throw new Állapot_kivétel("saját JVM의 magyar gomb generálás 기능이 필요합니다.");
    }
    public native void 동작맡기기(동작받이 받이);
}
