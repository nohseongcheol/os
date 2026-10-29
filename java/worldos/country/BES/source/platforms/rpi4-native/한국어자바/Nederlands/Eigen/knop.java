// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;
/** Eigen 화면에서 Actie 알림을 보내는 knop. */
public final class knop extends scherm_element {
    public knop(String tekst, int 가로, int Verticaal_functie, int 폭, int hoogte_WAARDE, 동작받이 받이) {
        throw new Status_uitzondering("Eigen JVM의 Nederlands knop genereren 기능이 필요합니다.");
    }
    public native void 동작맡기기(동작받이 받이);
}
