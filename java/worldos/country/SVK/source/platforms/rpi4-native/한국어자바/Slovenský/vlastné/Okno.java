// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;
/** vlastné JVM과 커널의 Okno 관리 기능에 직접 연결되는 Okno. */
public final class Okno extends 화면구성요소 {
    public Okno(String okno_Názov, int 폭, int výška_VALUE) {
        throw new Stav_výnimka("vlastné JVM의 Slovenský Okno generovať 기능이 필요합니다.");
    }
    public native void Pridať_prvok(화면구성요소 prvok_VALUE);
    public native void zobraziť_okno();
    public native void Zatvoriť();
    public native boolean 보이는가();
}
