// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;
/** 화면(畫面): 부팅 때 선택한 크기의 자체 kernel_VALOR RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int VALOR = kernel_VALOR.화면너비(); if (VALOR < 0) throw new Estado_excepción("프레임버퍼 없음"); return VALOR; }
    public static int 높이() { int VALOR = kernel_VALOR.화면높이(); if (VALOR < 0) throw new Estado_excepción("프레임버퍼 없음"); return VALOR; }
    public static void 사각형(int 가로, int Vertical_cargo, int 폭, int 높이, int 색) {
        if (가로 < 0 || Vertical_cargo < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || Vertical_cargo > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - Vertical_cargo) throw new non_válido_argumento_excepción("화면 clip");
        if (kernel_VALOR.사각형(가로, Vertical_cargo, 폭, 높이, 색) < 0) throw new Estado_excepción("프레임버퍼 없음");
    }
    public static void borrar_introdución(int 색) { 사각형(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (kernel_VALOR.그림대기() < 0) throw new Estado_excepción("interactivo 입력 필요"); }
}
