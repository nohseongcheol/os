// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;
/** 화면(畫面): 부팅 때 선택한 크기의 निज कर्नेल_मान RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int मान = कर्नेल_मान.화면너비(); if (मान < 0) throw new अवस्था_अपवाद("프레임버퍼 없음"); return मान; }
    public static int 높이() { int मान = कर्नेल_मान.화면높이(); if (मान < 0) throw new अवस्था_अपवाद("프레임버퍼 없음"); return मान; }
    public static void रेक्_टेंगल(int 가로, int अनुलंब_पद, int 폭, int 높이, int 색) {
        if (가로 < 0 || अनुलंब_पद < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || अनुलंब_पद > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - अनुलंब_पद) throw new अमान्य_तर्क_अपवाद("화면 क्लिप");
        if (कर्नेल_मान.रेक्_टेंगल(가로, अनुलंब_पद, 폭, 높이, 색) < 0) throw new अवस्था_अपवाद("프레임버퍼 없음");
    }
    public static void मिटाएँ_एन्ट्री(int 색) { रेक्_टेंगल(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (कर्नेल_मान.그림대기() < 0) throw new अवस्था_अपवाद("대화형 입력 필요"); }
}
