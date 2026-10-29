// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;
/** vlastní JVM과 커널의 Okno 관리 기능에 직접 연결되는 Okno. */
public final class Okno extends 화면구성요소 {
    public Okno(String okno_Název, int 폭, int výška_HODNOTA) {
        throw new Stav_výjimka("vlastní JVM의 čeština Okno generovat 기능이 필요합니다.");
    }
    public native void Přidat_prvek(화면구성요소 prvek_HODNOTA);
    public native void zobrazit_okno();
    public native void Zavřené();
    public native boolean 보이는가();
}
