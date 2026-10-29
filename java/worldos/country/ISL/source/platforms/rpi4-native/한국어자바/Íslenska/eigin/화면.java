// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;
/** 화면(畫面): 부팅 때 선택한 크기의 eigin kjarni_VALUE RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int VALUE = kjarni_VALUE.화면너비(); if (VALUE < 0) throw new staða_undantekning("프레임버퍼 없음"); return VALUE; }
    public static int 높이() { int VALUE = kjarni_VALUE.화면높이(); if (VALUE < 0) throw new staða_undantekning("프레임버퍼 없음"); return VALUE; }
    public static void 사각형(int 가로, int Lóðrétt_staða, int 폭, int 높이, int 색) {
        if (가로 < 0 || Lóðrétt_staða < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || Lóðrétt_staða > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - Lóðrétt_staða) throw new ógilt_frumbreyta_undantekning("화면 miðlaskrá");
        if (kjarni_VALUE.사각형(가로, Lóðrétt_staða, 폭, 높이, 색) < 0) throw new staða_undantekning("프레임버퍼 없음");
    }
    public static void eyða_færsla(int 색) { 사각형(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (kjarni_VALUE.그림대기() < 0) throw new staða_undantekning("gagnvirkur 입력 필요"); }
}
