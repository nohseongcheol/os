// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Suomi.JFinOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class merkki_näyttö {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int toimiala_toimi;

    public merkki_näyttö() {
        poistaa_merkintä_c8dbc399();
    }

    public void tulostuspaikka(String Sisältö_ARVO) {
        for (int INDEKSI = 0; INDEKSI < Sisältö_ARVO.length(); INDEKSI++) {
            char 문자 = Sisältö_ARVO.charAt(INDEKSI);
            if (문자 == '\n') {
                가로 = 0;
                toimiala_toimi++;
            } else {
                문자출력(가로++, toimiala_toimi, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                toimiala_toimi++;
            }
            if (toimiala_toimi >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int toimiala_toimi) {
        tarkistaa_toimi(가로, toimiala_toimi);
        return 문자들[toimiala_toimi * 너비 + 가로];
    }

    public void poistaa_merkintä_c8dbc399() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        toimiala_toimi = 0;
    }

    private void 문자출력(int 가로, int toimiala_toimi, char 문자) {
        tarkistaa_toimi(가로, toimiala_toimi);
        문자들[toimiala_toimi * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        toimiala_toimi = 높이 - 1;
    }

    private void tarkistaa_toimi(int 가로, int toimiala_toimi) {
        if (가로 < 0 || 가로 >= 너비 || toimiala_toimi < 0 || toimiala_toimi >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

