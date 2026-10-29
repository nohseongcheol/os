// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;
/** eget 화면에서 Handling 알림을 보내는 Knapp. */
public final class Knapp extends skjermbilde_element {
    public Knapp(String Tekst, int 가로, int vertikal_plassere, int 폭, int 높이, 동작받이 받이) {
        throw new status_unntak("eget JVM의 norsk Knapp generere 기능이 필요합니다.");
    }
    public native void 동작맡기기(동작받이 받이);
}
