// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;
/** 화면(畫面): 부팅 때 선택한 크기의 propriu nucleu_VALUE RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int VALUE = nucleu_VALUE.화면너비(); if (VALUE < 0) throw new Stare_excepție("프레임버퍼 없음"); return VALUE; }
    public static int 높이() { int VALUE = nucleu_VALUE.화면높이(); if (VALUE < 0) throw new Stare_excepție("프레임버퍼 없음"); return VALUE; }
    public static void dreptunghi(int 가로, int Verticală_poziție, int 폭, int 높이, int 색) {
        if (가로 < 0 || Verticală_poziție < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || Verticală_poziție > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - Verticală_poziție) throw new nul_argument_excepție("화면 clip");
        if (nucleu_VALUE.dreptunghi(가로, Verticală_poziție, 폭, 높이, 색) < 0) throw new Stare_excepție("프레임버퍼 없음");
    }
    public static void șterge_intrare(int 색) { dreptunghi(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (nucleu_VALUE.그림대기() < 0) throw new Stare_excepție("대화형 입력 필요"); }
}
