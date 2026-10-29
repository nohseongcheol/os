// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;
/** 화면(畫面): 부팅 때 선택한 크기의 자체 nukleo_balio RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int balio = nukleo_balio.화면너비(); if (balio < 0) throw new Egoera_salbuespen("프레임버퍼 없음"); return balio; }
    public static int 높이() { int balio = nukleo_balio.화면높이(); if (balio < 0) throw new Egoera_salbuespen("프레임버퍼 없음"); return balio; }
    public static void 사각형(int 가로, int Bertikala_kargu, int 폭, int 높이, int 색) {
        if (가로 < 0 || Bertikala_kargu < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || Bertikala_kargu > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - Bertikala_kargu) throw new baliogabe_arg_salbuespen("화면 klip");
        if (nukleo_balio.사각형(가로, Bertikala_kargu, 폭, 높이, 색) < 0) throw new Egoera_salbuespen("프레임버퍼 없음");
    }
    public static void ezabatu_sarrera(int 색) { 사각형(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (nukleo_balio.그림대기() < 0) throw new Egoera_salbuespen("interaktibo 입력 필요"); }
}
