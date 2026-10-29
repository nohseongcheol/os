// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malta.JMltOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class karattru_wera {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int Vertikali_pożizzjoni;

    public karattru_wera() {
        지우기();
    }

    public void 출력(String Kontenut_VALUE) {
        for (int INDEX = 0; INDEX < Kontenut_VALUE.length(); INDEX++) {
            char 문자 = Kontenut_VALUE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                Vertikali_pożizzjoni++;
            } else {
                문자출력(가로++, Vertikali_pożizzjoni, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Vertikali_pożizzjoni++;
            }
            if (Vertikali_pożizzjoni >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Vertikali_pożizzjoni) {
        vverifika_pożizzjoni(가로, Vertikali_pożizzjoni);
        return 문자들[Vertikali_pożizzjoni * 너비 + 가로];
    }

    public void 지우기() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Vertikali_pożizzjoni = 0;
    }

    private void 문자출력(int 가로, int Vertikali_pożizzjoni, char 문자) {
        vverifika_pożizzjoni(가로, Vertikali_pożizzjoni);
        문자들[Vertikali_pożizzjoni * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        Vertikali_pożizzjoni = 높이 - 1;
    }

    private void vverifika_pożizzjoni(int 가로, int Vertikali_pożizzjoni) {
        if (가로 < 0 || 가로 >= 너비 || Vertikali_pożizzjoni < 0 || Vertikali_pożizzjoni >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

