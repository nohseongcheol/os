// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자체;
/** 자체 커널의 표준 ಔಟ್_ಪುಟ್. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class ಔಟ್_ಪುಟ್ {
    private ಔಟ್_ಪುಟ್() {}
    public static void ಬರೆ(String ಪಠ್ಯ) { System.out.print(ಪಠ್ಯ); }
    public static void ಬರೆ_ಸಾಲು(String ಪಠ್ಯ) { System.out.println(ಪಠ್ಯ); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
