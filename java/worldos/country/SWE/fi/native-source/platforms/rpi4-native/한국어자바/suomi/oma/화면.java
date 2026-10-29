// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;
/** 화면(畫面): koneen_käynnistys 때 선택한 크기의 oma ydin_ARVO RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int ARVO = ydin_ARVO.화면너비(); if (ARVO < 0) throw new Tila_poikkeus("프레임버퍼 없음"); return ARVO; }
    public static int 높이() { int ARVO = ydin_ARVO.화면높이(); if (ARVO < 0) throw new Tila_poikkeus("프레임버퍼 없음"); return ARVO; }
    public static void suorakulmio(int 가로, int toimiala_toimi, int 폭, int 높이, int 색) {
        if (가로 < 0 || toimiala_toimi < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || toimiala_toimi > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - toimiala_toimi) throw new pätemätön_argumentti_poikkeus("화면 leikata");
        if (ydin_ARVO.suorakulmio(가로, toimiala_toimi, 폭, 높이, 색) < 0) throw new Tila_poikkeus("프레임버퍼 없음");
    }
    public static void poistaa_merkintä_c8dbc399(int 색) { suorakulmio(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (ydin_ARVO.그림대기() < 0) throw new Tila_poikkeus("vuorovaikutteinen syöte_ARVO 필요"); }
}
