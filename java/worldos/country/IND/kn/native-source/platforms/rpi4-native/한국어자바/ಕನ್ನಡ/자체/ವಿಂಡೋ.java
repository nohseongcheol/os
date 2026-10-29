// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자체;
/** 자체 JVM과 커널의 ವಿಂಡೋ 관리 기능에 직접 연결되는 ವಿಂಡೋ. */
public final class ವಿಂಡೋ extends 화면구성요소 {
    public ವಿಂಡೋ(String ವಿಂಡೋ_ಶೀರ್ಷಿಕೆ, int 폭, int 높이) {
        throw new ಸ್ಥಿತಿ_ವಿನಾಯಿತಿ("자체 JVM의 ಕನ್ನಡ ವಿಂಡೋ ರಚಿಸಿ 기능이 필요합니다.");
    }
    public native void ಸಂಕಲನ_ಮೂಲಾಂಶ(화면구성요소 ಮೂಲಾಂಶ_ಮೌಲ್ಯ);
    public native void ಶೋ_ವಿಂಡೋ();
    public native void ಮುಚ್ಚು();
    public native boolean 보이는가();
}
