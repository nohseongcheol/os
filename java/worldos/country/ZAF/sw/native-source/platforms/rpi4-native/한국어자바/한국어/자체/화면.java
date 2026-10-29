// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 화면(畫面): 부팅 때 선택한 크기의 자체 kiini_thamani_0611a8a8 RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int thamani = kiini_thamani_0611a8a8.화면너비(); if (thamani < 0) throw new hali_vighairi("프레임버퍼 없음"); return thamani; }
    public static int 높이() { int thamani = kiini_thamani_0611a8a8.화면높이(); if (thamani < 0) throw new hali_vighairi("프레임버퍼 없음"); return thamani; }
    public static void 사각형(int 가로, int 세로, int 폭, int 높이, int 색) {
        if (가로 < 0 || 세로 < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || 세로 > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - 세로) throw new batili_hoja_vighairi("화면 dondoo");
        if (kiini_thamani_0611a8a8.사각형(가로, 세로, 폭, 높이, 색) < 0) throw new hali_vighairi("프레임버퍼 없음");
    }
    public static void futa_ingizo(int 색) { 사각형(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (kiini_thamani_0611a8a8.그림대기() < 0) throw new hali_vighairi("ingiliani 입력 필요"); }
}
