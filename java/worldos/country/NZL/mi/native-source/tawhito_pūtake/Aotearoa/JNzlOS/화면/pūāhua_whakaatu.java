// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aotearoa.JNzlOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class pūāhua_whakaatu {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int Poutū_tūranga;

    public pūāhua_whakaatu() {
        지우기();
    }

    public void 출력(String Ihirangi_uara) {
        for (int INDEX = 0; INDEX < Ihirangi_uara.length(); INDEX++) {
            char 문자 = Ihirangi_uara.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                Poutū_tūranga++;
            } else {
                문자출력(가로++, Poutū_tūranga, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Poutū_tūranga++;
            }
            if (Poutū_tūranga >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Poutū_tūranga) {
        manatoko_tūranga(가로, Poutū_tūranga);
        return 문자들[Poutū_tūranga * 너비 + 가로];
    }

    public void 지우기() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Poutū_tūranga = 0;
    }

    private void 문자출력(int 가로, int Poutū_tūranga, char 문자) {
        manatoko_tūranga(가로, Poutū_tūranga);
        문자들[Poutū_tūranga * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        Poutū_tūranga = 높이 - 1;
    }

    private void manatoko_tūranga(int 가로, int Poutū_tūranga) {
        if (가로 < 0 || 가로 >= 너비 || Poutū_tūranga < 0 || Poutū_tūranga >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

