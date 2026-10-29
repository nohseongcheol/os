// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ikinyarwanda.자체;
/** 화면(畫面): 부팅 때 선택한 크기의 자체 intima_agaciro RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int agaciro = intima_agaciro.화면너비(); if (agaciro < 0) throw new 상태예외("프레임버퍼 없음"); return agaciro; }
    public static int 높이() { int agaciro = intima_agaciro.화면높이(); if (agaciro < 0) throw new 상태예외("프레임버퍼 없음"); return agaciro; }
    public static void 사각형(int 가로, int 세로, int 폭, int 높이, int 색) {
        if (가로 < 0 || 세로 < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || 세로 > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - 세로) throw new 잘못된인수예외("화면 kiripu");
        if (intima_agaciro.사각형(가로, 세로, 폭, 높이, 색) < 0) throw new 상태예외("프레임버퍼 없음");
    }
    public static void 지우기(int 색) { 사각형(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (intima_agaciro.그림대기() < 0) throw new 상태예외("interfacebikorana 입력 필요"); }
}
