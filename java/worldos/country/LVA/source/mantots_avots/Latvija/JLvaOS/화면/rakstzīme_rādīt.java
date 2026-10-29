// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class rakstzīme_rādīt {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int vertikāle_amats;

    public rakstzīme_rādīt() {
        dzēst_ievade();
    }

    public void Izvade(String Saturs_VALUE) {
        for (int INDEX = 0; INDEX < Saturs_VALUE.length(); INDEX++) {
            char 문자 = Saturs_VALUE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                vertikāle_amats++;
            } else {
                문자출력(가로++, vertikāle_amats, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                vertikāle_amats++;
            }
            if (vertikāle_amats >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int vertikāle_amats) {
        verificēt_amats(가로, vertikāle_amats);
        return 문자들[vertikāle_amats * 너비 + 가로];
    }

    public void dzēst_ievade() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        vertikāle_amats = 0;
    }

    private void 문자출력(int 가로, int vertikāle_amats, char 문자) {
        verificēt_amats(가로, vertikāle_amats);
        문자들[vertikāle_amats * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        vertikāle_amats = 높이 - 1;
    }

    private void verificēt_amats(int 가로, int vertikāle_amats) {
        if (가로 < 0 || 가로 >= 너비 || vertikāle_amats < 0 || vertikāle_amats >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

