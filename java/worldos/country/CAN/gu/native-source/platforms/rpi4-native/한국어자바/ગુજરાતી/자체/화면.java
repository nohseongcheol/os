// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자체;
/** 화면(畫面): 부팅 때 선택한 크기의 자체 કર્નેલ_મૂલ્ય RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int મૂલ્ય = કર્નેલ_મૂલ્ય.화면너비(); if (મૂલ્ય < 0) throw new 상태예외("프레임버퍼 없음"); return મૂલ્ય; }
    public static int 높이() { int મૂલ્ય = કર્નેલ_મૂલ્ય.화면높이(); if (મૂલ્ય < 0) throw new 상태예외("프레임버퍼 없음"); return મૂલ્ય; }
    public static void 사각형(int 가로, int ઊભી_સ્થિતિ, int 폭, int 높이, int 색) {
        if (가로 < 0 || ઊભી_સ્થિતિ < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || ઊભી_સ્થિતિ > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - ઊભી_સ્થિતિ) throw new 잘못된인수예외("화면 ક્લિપ");
        if (કર્નેલ_મૂલ્ય.사각형(가로, ઊભી_સ્થિતિ, 폭, 높이, 색) < 0) throw new 상태예외("프레임버퍼 없음");
    }
    public static void 지우기(int 색) { 사각형(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (કર્નેલ_મૂલ્ય.그림대기() < 0) throw new 상태예외("સહભાગી 입력 필요"); }
}
