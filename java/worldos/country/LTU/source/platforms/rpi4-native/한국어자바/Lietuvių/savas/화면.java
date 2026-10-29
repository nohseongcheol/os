// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;
/** 화면(畫面): 부팅 때 선택한 크기의 savas branduolys_VALUE RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int VALUE = branduolys_VALUE.화면너비(); if (VALUE < 0) throw new Būsena_išimtis("프레임버퍼 없음"); return VALUE; }
    public static int 높이() { int VALUE = branduolys_VALUE.화면높이(); if (VALUE < 0) throw new Būsena_išimtis("프레임버퍼 없음"); return VALUE; }
    public static void stačiakampis(int 가로, int segmentas_padėtis, int 폭, int 높이, int 색) {
        if (가로 < 0 || segmentas_padėtis < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || segmentas_padėtis > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - segmentas_padėtis) throw new neleistinas_argumentas_išimtis("화면 klipas");
        if (branduolys_VALUE.stačiakampis(가로, segmentas_padėtis, 폭, 높이, 색) < 0) throw new Būsena_išimtis("프레임버퍼 없음");
    }
    public static void ištrinti_įrašas(int 색) { stačiakampis(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (branduolys_VALUE.그림대기() < 0) throw new Būsena_išimtis("대화형 입력 필요"); }
}
