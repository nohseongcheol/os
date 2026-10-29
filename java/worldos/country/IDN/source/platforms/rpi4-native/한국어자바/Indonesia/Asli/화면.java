// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;
/** 화면(畫面): awal_mesin 때 선택한 크기의 Asli kernel_VALUE RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int VALUE = kernel_VALUE.화면너비(); if (VALUE < 0) throw new Status_pengecualian("프레임버퍼 없음"); return VALUE; }
    public static int 높이() { int VALUE = kernel_VALUE.화면높이(); if (VALUE < 0) throw new Status_pengecualian("프레임버퍼 없음"); return VALUE; }
    public static void persegi(int 가로, int Vertikal_posisi, int 폭, int 높이, int 색) {
        if (가로 < 0 || Vertikal_posisi < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || Vertikal_posisi > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - Vertikal_posisi) throw new tidak_sahih_argumen_pengecualian("화면 klip");
        if (kernel_VALUE.persegi(가로, Vertikal_posisi, 폭, 높이, 색) < 0) throw new Status_pengecualian("프레임버퍼 없음");
    }
    public static void hapus_entri_c8dbc399(int 색) { persegi(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (kernel_VALUE.그림대기() < 0) throw new Status_pengecualian("interaktif 입력 필요"); }
}
