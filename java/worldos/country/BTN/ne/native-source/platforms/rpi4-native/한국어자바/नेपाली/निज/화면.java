// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.निज;
/** 화면(畫面): 부팅 때 선택한 크기의 निज कर्णेल_मान RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int मान = कर्णेल_मान.화면너비(); if (मान < 0) throw new 상태예외("프레임버퍼 없음"); return मान; }
    public static int 높이() { int मान = कर्णेल_मान.화면높이(); if (मान < 0) throw new 상태예외("프레임버퍼 없음"); return मान; }
    public static void 사각형(int 가로, int ठाडो_राख्नुहोस्, int 폭, int 높이, int 색) {
        if (가로 < 0 || ठाडो_राख्नुहोस् < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || ठाडो_राख्नुहोस् > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - ठाडो_राख्नुहोस्) throw new 잘못된인수예외("화면 क्लिप");
        if (कर्णेल_मान.사각형(가로, ठाडो_राख्नुहोस्, 폭, 높이, 색) < 0) throw new 상태예외("프레임버퍼 없음");
    }
    public static void 지우기(int 색) { 사각형(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (कर्णेल_मान.그림대기() < 0) throw new 상태예외("अन्तरक्रियाशील 입력 필요"); }
}
