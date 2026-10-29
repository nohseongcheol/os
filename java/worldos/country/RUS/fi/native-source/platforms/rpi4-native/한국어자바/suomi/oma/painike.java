// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;
/** oma 화면에서 Toiminto 알림을 보내는 painike. */
public final class painike extends 화면구성요소 {
    public painike(String teksti, int 가로, int toimiala_toimi, int 폭, int 높이, 동작받이 받이) {
        throw new Tila_poikkeus("oma JVM의 suomi painike generoida 기능이 필요합니다.");
    }
    public native void 동작맡기기(동작받이 받이);
}
