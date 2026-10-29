// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class teikn_vise {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int vertikalvising_plassere;

    public teikn_vise() {
        지우기();
    }

    public void Utdata(String Innhald_VALUE) {
        for (int INDEX = 0; INDEX < Innhald_VALUE.length(); INDEX++) {
            char 문자 = Innhald_VALUE.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                vertikalvising_plassere++;
            } else {
                문자출력(가로++, vertikalvising_plassere, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                vertikalvising_plassere++;
            }
            if (vertikalvising_plassere >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int vertikalvising_plassere) {
        stadfeste_plassere(가로, vertikalvising_plassere);
        return 문자들[vertikalvising_plassere * 너비 + 가로];
    }

    public void 지우기() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        vertikalvising_plassere = 0;
    }

    private void 문자출력(int 가로, int vertikalvising_plassere, char 문자) {
        stadfeste_plassere(가로, vertikalvising_plassere);
        문자들[vertikalvising_plassere * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        vertikalvising_plassere = 높이 - 1;
    }

    private void stadfeste_plassere(int 가로, int vertikalvising_plassere) {
        if (가로 < 0 || 가로 >= 너비 || vertikalvising_plassere < 0 || vertikalvising_plassere >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

