// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Románia.JRouOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class karakter_kijelző {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int szektor_pozíció;

    public karakter_kijelző() {
        töröl_bejegyzés();
    }

    public void Kimenet(String Tartalom_ÉRTÉK) {
        for (int INDEX = 0; INDEX < Tartalom_ÉRTÉK.length(); INDEX++) {
            char 문자 = Tartalom_ÉRTÉK.charAt(INDEX);
            if (문자 == '\n') {
                가로 = 0;
                szektor_pozíció++;
            } else {
                문자출력(가로++, szektor_pozíció, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                szektor_pozíció++;
            }
            if (szektor_pozíció >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int szektor_pozíció) {
        igazol_pozíció(가로, szektor_pozíció);
        return 문자들[szektor_pozíció * 너비 + 가로];
    }

    public void töröl_bejegyzés() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        szektor_pozíció = 0;
    }

    private void 문자출력(int 가로, int szektor_pozíció, char 문자) {
        igazol_pozíció(가로, szektor_pozíció);
        문자들[szektor_pozíció * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        szektor_pozíció = 높이 - 1;
    }

    private void igazol_pozíció(int 가로, int szektor_pozíció) {
        if (가로 < 0 || 가로 >= 너비 || szektor_pozíció < 0 || szektor_pozíció >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

