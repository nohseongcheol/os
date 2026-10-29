// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;
/** własny JVM과 커널의 Okno 관리 기능에 직접 연결되는 Okno. */
public final class Okno extends 화면구성요소 {
    public Okno(String okno_Tytuł, int 폭, int wysokość_WARTOŚĆ) {
        throw new Stan_wyjątek("własny JVM의 polski Okno generować 기능이 필요합니다.");
    }
    public native void Dodaj_element(화면구성요소 element_WARTOŚĆ);
    public native void program_okno();
    public native void Zamknięte();
    public native boolean 보이는가();
}
