// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;
/** 화면(畫面): 부팅 때 선택한 크기의 propi nucli_VALOR RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int VALOR = nucli_VALOR.화면너비(); if (VALOR < 0) throw new Estat_excepció("프레임버퍼 없음"); return VALOR; }
    public static int 높이() { int VALOR = nucli_VALOR.화면높이(); if (VALOR < 0) throw new Estat_excepció("프레임버퍼 없음"); return VALOR; }
    public static void 사각형(int 가로, int Vertical_càrrec, int 폭, int 높이, int 색) {
        if (가로 < 0 || Vertical_càrrec < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || Vertical_càrrec > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - Vertical_càrrec) throw new invàlid_arg_excepció("화면 clip");
        if (nucli_VALOR.사각형(가로, Vertical_càrrec, 폭, 높이, 색) < 0) throw new Estat_excepció("프레임버퍼 없음");
    }
    public static void esborrar_introducció(int 색) { 사각형(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (nucli_VALOR.그림대기() < 0) throw new Estat_excepció("interactiu 입력 필요"); }
}
