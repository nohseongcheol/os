// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;
/** lastno JVM과 커널의 okno 관리 기능에 직접 연결되는 okno. */
public final class okno extends 화면구성요소 {
    public okno(String okno_naslov, int 폭, int višina_VALUE) {
        throw new stanje_izjema("lastno JVM의 slovenščina okno ustvariti 기능이 필요합니다.");
    }
    public native void Dodaj_element(화면구성요소 element_VALUE);
    public native void oddaja_okno();
    public native void Zapri();
    public native boolean 보이는가();
}
