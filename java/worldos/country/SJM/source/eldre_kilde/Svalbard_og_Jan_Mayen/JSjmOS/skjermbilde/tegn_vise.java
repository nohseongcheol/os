// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svalbard_og_Jan_Mayen.JSjmOS.skjermbilde;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 skjermbilde 모형이다. */
public final class tegn_vise {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int vertikal_plassere;

    public tegn_vise() {
        slette_oppføring();
    }

    public void Utgang(String Innhold_VERDI) {
        for (int INDEKS = 0; INDEKS < Innhold_VERDI.length(); INDEKS++) {
            char 문자 = Innhold_VERDI.charAt(INDEKS);
            if (문자 == '\n') {
                가로 = 0;
                vertikal_plassere++;
            } else {
                문자출력(가로++, vertikal_plassere, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                vertikal_plassere++;
            }
            if (vertikal_plassere >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int vertikal_plassere) {
        bekrefte_plassere(가로, vertikal_plassere);
        return 문자들[vertikal_plassere * 너비 + 가로];
    }

    public void slette_oppføring() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        vertikal_plassere = 0;
    }

    private void 문자출력(int 가로, int vertikal_plassere, char 문자) {
        bekrefte_plassere(가로, vertikal_plassere);
        문자들[vertikal_plassere * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        vertikal_plassere = 높이 - 1;
    }

    private void bekrefte_plassere(int 가로, int vertikal_plassere) {
        if (가로 < 0 || 가로 >= 너비 || vertikal_plassere < 0 || vertikal_plassere >= 높이) {
            throw new IllegalArgumentException("skjermbilde 위치가 올바르지 않습니다.");
        }
    }
}

