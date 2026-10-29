// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;
/** 화면(畫面): 부팅 때 선택한 크기의 vlastné jadro_VALUE RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int VALUE = jadro_VALUE.화면너비(); if (VALUE < 0) throw new Stav_výnimka("프레임버퍼 없음"); return VALUE; }
    public static int výška_VALUE() { int VALUE = jadro_VALUE.화면높이(); if (VALUE < 0) throw new Stav_výnimka("프레임버퍼 없음"); return VALUE; }
    public static void obdĺžnik(int 가로, int vertikála_pozícia, int 폭, int výška_VALUE, int 색) {
        if (가로 < 0 || vertikála_pozícia < 0 || 폭 < 0 || výška_VALUE < 0 || 가로 > 너비() || vertikála_pozícia > výška_VALUE() || 폭 > 너비() - 가로 || výška_VALUE > výška_VALUE() - vertikála_pozícia) throw new neplatné_argument_výnimka("화면 klip");
        if (jadro_VALUE.obdĺžnik(가로, vertikála_pozícia, 폭, výška_VALUE, 색) < 0) throw new Stav_výnimka("프레임버퍼 없음");
    }
    public static void vymazať_položka(int 색) { obdĺžnik(0, 0, 너비(), výška_VALUE(), 색); }
    public static void 기다리기() { if (jadro_VALUE.그림대기() < 0) throw new Stav_výnimka("interaktívny vstup_VALUE 필요"); }
}
