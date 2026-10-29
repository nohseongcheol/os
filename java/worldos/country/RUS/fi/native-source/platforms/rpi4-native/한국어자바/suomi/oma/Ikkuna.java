// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;
/** oma JVM과 커널의 Ikkuna 관리 기능에 직접 연결되는 Ikkuna. */
public final class Ikkuna extends 화면구성요소 {
    public Ikkuna(String ikkuna_nimi, int 폭, int 높이) {
        throw new Tila_poikkeus("oma JVM의 suomi Ikkuna generoida 기능이 필요합니다.");
    }
    public native void Lisää_elementti(화면구성요소 elementti_ARVO);
    public native void näyttää_ikkuna();
    public native void Sulje();
    public native boolean 보이는가();
}
