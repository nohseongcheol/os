// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자체;
/** 화면(畫面): 부팅 때 선택한 크기의 자체 ಕರ್ನಲ್_ಮೌಲ್ಯ RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int ಮೌಲ್ಯ = ಕರ್ನಲ್_ಮೌಲ್ಯ.화면너비(); if (ಮೌಲ್ಯ < 0) throw new ಸ್ಥಿತಿ_ವಿನಾಯಿತಿ("프레임버퍼 없음"); return ಮೌಲ್ಯ; }
    public static int 높이() { int ಮೌಲ್ಯ = ಕರ್ನಲ್_ಮೌಲ್ಯ.화면높이(); if (ಮೌಲ್ಯ < 0) throw new ಸ್ಥಿತಿ_ವಿನಾಯಿತಿ("프레임버퍼 없음"); return ಮೌಲ್ಯ; }
    public static void 사각형(int 가로, int ಲಂಬ_ಹುದ್ದೆ, int 폭, int 높이, int 색) {
        if (가로 < 0 || ಲಂಬ_ಹುದ್ದೆ < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || ಲಂಬ_ಹುದ್ದೆ > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - ಲಂಬ_ಹುದ್ದೆ) throw new ಅಮಾನ್ಯ_ವಾದ_ವಿನಾಯಿತಿ("화면 ಕ್ಲಿಪ್");
        if (ಕರ್ನಲ್_ಮೌಲ್ಯ.사각형(가로, ಲಂಬ_ಹುದ್ದೆ, 폭, 높이, 색) < 0) throw new ಸ್ಥಿತಿ_ವಿನಾಯಿತಿ("프레임버퍼 없음");
    }
    public static void ಅಳಿಸು_ನಮೂದು(int 색) { 사각형(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (ಕರ್ನಲ್_ಮೌಲ್ಯ.그림대기() < 0) throw new ಸ್ಥಿತಿ_ವಿನಾಯಿತಿ("ಸಂವಾದಕ 입력 필요"); }
}
