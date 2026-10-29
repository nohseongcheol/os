// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkiyə.JTurOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class simvol_displey {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int Şaquli_yerinə_qoymaq;

    public simvol_displey() {
        silmək_daxiletmə_c8dbc399();
    }

    public void 출력(String Məzmun_VALUE) {
        for (int INDEX = 0; INDEX < Məzmun_VALUE.length(); INDEX++) {
            char 문자 = Məzmun_VALUE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                Şaquli_yerinə_qoymaq++;
            } else {
                문자출력(가로++, Şaquli_yerinə_qoymaq, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Şaquli_yerinə_qoymaq++;
            }
            if (Şaquli_yerinə_qoymaq >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Şaquli_yerinə_qoymaq) {
        yoxlamaq_yerinə_qoymaq(가로, Şaquli_yerinə_qoymaq);
        return 문자들[Şaquli_yerinə_qoymaq * 너비 + 가로];
    }

    public void silmək_daxiletmə_c8dbc399() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Şaquli_yerinə_qoymaq = 0;
    }

    private void 문자출력(int 가로, int Şaquli_yerinə_qoymaq, char 문자) {
        yoxlamaq_yerinə_qoymaq(가로, Şaquli_yerinə_qoymaq);
        문자들[Şaquli_yerinə_qoymaq * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        Şaquli_yerinə_qoymaq = 높이 - 1;
    }

    private void yoxlamaq_yerinə_qoymaq(int 가로, int Şaquli_yerinə_qoymaq) {
        if (가로 < 0 || 가로 >= 너비 || Şaquli_yerinə_qoymaq < 0 || Şaquli_yerinə_qoymaq >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

