// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 화면(畫面): 부팅 때 선택한 크기의 자체 bërthamë_VALUE RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int VALUE = bërthamë_VALUE.화면너비(); if (VALUE < 0) throw new status_përjashtim("프레임버퍼 없음"); return VALUE; }
    public static int 높이() { int VALUE = bërthamë_VALUE.화면높이(); if (VALUE < 0) throw new status_përjashtim("프레임버퍼 없음"); return VALUE; }
    public static void 사각형(int 가로, int Vertikal_pozicioni, int 폭, int 높이, int 색) {
        if (가로 < 0 || Vertikal_pozicioni < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || Vertikal_pozicioni > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - Vertikal_pozicioni) throw new i_pavlefshëm_argument_përjashtim("화면 fragment");
        if (bërthamë_VALUE.사각형(가로, Vertikal_pozicioni, 폭, 높이, 색) < 0) throw new status_përjashtim("프레임버퍼 없음");
    }
    public static void spastroj_futje(int 색) { 사각형(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (bërthamë_VALUE.그림대기() < 0) throw new status_përjashtim("ndërvepruese 입력 필요"); }
}
