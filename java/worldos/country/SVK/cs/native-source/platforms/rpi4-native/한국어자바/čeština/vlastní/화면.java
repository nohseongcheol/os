// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;
/** 화면(畫面): spuštění_stroje 때 선택한 크기의 vlastní jádro_HODNOTA RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int HODNOTA = jádro_HODNOTA.화면너비(); if (HODNOTA < 0) throw new Stav_výjimka("프레임버퍼 없음"); return HODNOTA; }
    public static int výška_HODNOTA() { int HODNOTA = jádro_HODNOTA.화면높이(); if (HODNOTA < 0) throw new Stav_výjimka("프레임버퍼 없음"); return HODNOTA; }
    public static void obdélník(int 가로, int Svislá_pozice, int 폭, int výška_HODNOTA, int 색) {
        if (가로 < 0 || Svislá_pozice < 0 || 폭 < 0 || výška_HODNOTA < 0 || 가로 > 너비() || Svislá_pozice > výška_HODNOTA() || 폭 > 너비() - 가로 || výška_HODNOTA > výška_HODNOTA() - Svislá_pozice) throw new neplatný_argument_výjimka("화면 oříznout");
        if (jádro_HODNOTA.obdélník(가로, Svislá_pozice, 폭, výška_HODNOTA, 색) < 0) throw new Stav_výjimka("프레임버퍼 없음");
    }
    public static void vymazat_položka(int 색) { obdélník(0, 0, 너비(), výška_HODNOTA(), 색); }
    public static void 기다리기() { if (jádro_HODNOTA.그림대기() < 0) throw new Stav_výjimka("interaktivní vstup_HODNOTA 필요"); }
}
