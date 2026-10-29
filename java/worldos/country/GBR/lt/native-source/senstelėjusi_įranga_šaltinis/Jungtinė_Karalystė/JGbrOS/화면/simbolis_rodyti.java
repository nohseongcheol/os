// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Jungtinė_Karalystė.JGbrOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class simbolis_rodyti {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int segmentas_padėtis;

    public simbolis_rodyti() {
        ištrinti_įrašas();
    }

    public void Išvestis(String Turinys_VALUE) {
        for (int INDEX = 0; INDEX < Turinys_VALUE.length(); INDEX++) {
            char 문자 = Turinys_VALUE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                segmentas_padėtis++;
            } else {
                문자출력(가로++, segmentas_padėtis, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                segmentas_padėtis++;
            }
            if (segmentas_padėtis >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int segmentas_padėtis) {
        patvirtinti_padėtis(가로, segmentas_padėtis);
        return 문자들[segmentas_padėtis * 너비 + 가로];
    }

    public void ištrinti_įrašas() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        segmentas_padėtis = 0;
    }

    private void 문자출력(int 가로, int segmentas_padėtis, char 문자) {
        patvirtinti_padėtis(가로, segmentas_padėtis);
        문자들[segmentas_padėtis * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        segmentas_padėtis = 높이 - 1;
    }

    private void patvirtinti_padėtis(int 가로, int segmentas_padėtis) {
        if (가로 < 0 || 가로 >= 너비 || segmentas_padėtis < 0 || segmentas_padėtis >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

