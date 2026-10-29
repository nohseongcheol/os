// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಭಾರತ.JIndOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class ಅಕ್ಷರ_ಪ್ರದರ್ಶನ {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int ಲಂಬ_ಹುದ್ದೆ;

    public ಅಕ್ಷರ_ಪ್ರದರ್ಶನ() {
        ಅಳಿಸು_ನಮೂದು();
    }

    public void ಔಟ್_ಪುಟ್(String ವಿಷಯ_ಮೌಲ್ಯ) {
        for (int ಪದಸೂಚಿ = 0; ಪದಸೂಚಿ < ವಿಷಯ_ಮೌಲ್ಯ.length(); ಪದಸೂಚಿ++) {
            char 문자 = ವಿಷಯ_ಮೌಲ್ಯ.charAt(ಪದಸೂಚಿ);
            if (문자 == '\n') {
                가로 = 0;
                ಲಂಬ_ಹುದ್ದೆ++;
            } else {
                문자출력(가로++, ಲಂಬ_ಹುದ್ದೆ, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                ಲಂಬ_ಹುದ್ದೆ++;
            }
            if (ಲಂಬ_ಹುದ್ದೆ >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int ಲಂಬ_ಹುದ್ದೆ) {
        ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು_ಹುದ್ದೆ(가로, ಲಂಬ_ಹುದ್ದೆ);
        return 문자들[ಲಂಬ_ಹುದ್ದೆ * 너비 + 가로];
    }

    public void ಅಳಿಸು_ನಮೂದು() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        ಲಂಬ_ಹುದ್ದೆ = 0;
    }

    private void 문자출력(int 가로, int ಲಂಬ_ಹುದ್ದೆ, char 문자) {
        ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು_ಹುದ್ದೆ(가로, ಲಂಬ_ಹುದ್ದೆ);
        문자들[ಲಂಬ_ಹುದ್ದೆ * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        ಲಂಬ_ಹುದ್ದೆ = 높이 - 1;
    }

    private void ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು_ಹುದ್ದೆ(int 가로, int ಲಂಬ_ಹುದ್ದೆ) {
        if (가로 < 0 || 가로 >= 너비 || ಲಂಬ_ಹುದ್ದೆ < 0 || ಲಂಬ_ಹುದ್ದೆ >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

