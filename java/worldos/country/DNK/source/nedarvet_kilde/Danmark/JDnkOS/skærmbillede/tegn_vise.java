// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Danmark.JDnkOS.skærmbillede;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 skærmbillede 모형이다. */
public final class tegn_vise {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int Lodret_placere;

    public tegn_vise() {
        slette_post();
    }

    public void Udgang(String Indhold_VÆRDI) {
        for (int INDEKS = 0; INDEKS < Indhold_VÆRDI.length(); INDEKS++) {
            char 문자 = Indhold_VÆRDI.charAt(INDEKS);
            if (문자 == '\n') {
                가로 = 0;
                Lodret_placere++;
            } else {
                문자출력(가로++, Lodret_placere, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                Lodret_placere++;
            }
            if (Lodret_placere >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int Lodret_placere) {
        bekræfte_placere(가로, Lodret_placere);
        return 문자들[Lodret_placere * 너비 + 가로];
    }

    public void slette_post() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        Lodret_placere = 0;
    }

    private void 문자출력(int 가로, int Lodret_placere, char 문자) {
        bekræfte_placere(가로, Lodret_placere);
        문자들[Lodret_placere * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        Lodret_placere = 높이 - 1;
    }

    private void bekræfte_placere(int 가로, int Lodret_placere) {
        if (가로 < 0 || 가로 >= 너비 || Lodret_placere < 0 || Lodret_placere >= 높이) {
            throw new IllegalArgumentException("skærmbillede 위치가 올바르지 않습니다.");
        }
    }
}

