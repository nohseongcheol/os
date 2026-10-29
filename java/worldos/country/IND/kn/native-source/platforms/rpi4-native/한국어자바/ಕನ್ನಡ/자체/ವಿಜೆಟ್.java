// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자체;
/** ಕನ್ನಡ 화면 구성요소를 만드는 편의 ಕಾರ್ಯ_ಮೌಲ್ಯ. */
public final class ವಿಜೆಟ್ {
    private ವಿಜೆಟ್() {}
    public static void 나중에실행(실행할일 ಕಾರ್ಯ_ಕ್ರಿಯೆ) { ಸಂಗತಿ_ಸರದಿ.나중에실행(ಕಾರ್ಯ_ಕ್ರಿಯೆ); }
    public static ಲೇಬಲ್ ಟ್ಯಾಗ್_ಮೌಲ್ಯ(String ಪಠ್ಯ, int 가로, int ಲಂಬ_ಹುದ್ದೆ, int 폭, int 높이) {
        return new ಲೇಬಲ್(ಪಠ್ಯ, 가로, ಲಂಬ_ಹುದ್ದೆ, 폭, 높이);
    }
    public static ಬಟನ್ ಬಟನ್(String ಪಠ್ಯ, int 가로, int ಲಂಬ_ಹುದ್ದೆ, int 폭, int 높이, 동작받이 받이) {
        return new ಬಟನ್(ಪಠ್ಯ, 가로, ಲಂಬ_ಹುದ್ದೆ, 폭, 높이, 받이);
    }
    public static ಪಠ್ಯ_ಕ್ಷೇತ್ರ ಪಠ್ಯ_ಕ್ಷೇತ್ರ(String ಪಠ್ಯ, int 가로, int ಲಂಬ_ಹುದ್ದೆ, int 폭, int 높이) {
        return new ಪಠ್ಯ_ಕ್ಷೇತ್ರ(ಪಠ್ಯ, 가로, ಲಂಬ_ಹುದ್ದೆ, 폭, 높이);
    }
}
