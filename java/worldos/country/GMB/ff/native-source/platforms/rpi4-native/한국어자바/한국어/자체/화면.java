// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 화면(畫面): 부팅 때 선택한 크기의 자체 aaluude_njaru RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int njaru = aaluude_njaru.화면너비(); if (njaru < 0) throw new 상태예외("프레임버퍼 없음"); return njaru; }
    public static int 높이() { int njaru = aaluude_njaru.화면높이(); if (njaru < 0) throw new 상태예외("프레임버퍼 없음"); return njaru; }
    public static void 사각형(int 가로, int 세로, int 폭, int 높이, int 색) {
        if (가로 < 0 || 세로 < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || 세로 > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - 세로) throw new 잘못된인수예외("화면 kilip");
        if (aaluude_njaru.사각형(가로, 세로, 폭, 높이, 색) < 0) throw new 상태예외("프레임버퍼 없음");
    }
    public static void 지우기(int 색) { 사각형(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (aaluude_njaru.그림대기() < 0) throw new 상태예외("jokkondirtoo 입력 필요"); }
}
