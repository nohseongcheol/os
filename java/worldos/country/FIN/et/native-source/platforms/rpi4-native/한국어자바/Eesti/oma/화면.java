// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;
/** 화면(畫面): 부팅 때 선택한 크기의 oma tuum_VALUE RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int VALUE = tuum_VALUE.화면너비(); if (VALUE < 0) throw new Olek_erand("프레임버퍼 없음"); return VALUE; }
    public static int 높이() { int VALUE = tuum_VALUE.화면높이(); if (VALUE < 0) throw new Olek_erand("프레임버퍼 없음"); return VALUE; }
    public static void ristkülik(int 가로, int vertikaal_ametikoht, int 폭, int 높이, int 색) {
        if (가로 < 0 || vertikaal_ametikoht < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || vertikaal_ametikoht > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - vertikaal_ametikoht) throw new kehtetu_argument_erand("화면 klipp");
        if (tuum_VALUE.ristkülik(가로, vertikaal_ametikoht, 폭, 높이, 색) < 0) throw new Olek_erand("프레임버퍼 없음");
    }
    public static void kustutama_kirje(int 색) { ristkülik(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (tuum_VALUE.그림대기() < 0) throw new Olek_erand("대화형 입력 필요"); }
}
